# File: gk6/core.py

import json
import re


def list_apis(postman_collection):
    apis = []

    def extract_requests(items):
        for item in items:
            if "request" in item:
                apis.append(
                    {
                        "name": item["name"],
                        "method": item["request"]["method"],
                        "url": item["request"]["url"]["raw"],
                    }
                )
            elif "item" in item:
                extract_requests(item["item"])

    extract_requests(postman_collection["item"])
    return apis


def extract_chaining_variables(postman_collection):
    chaining_vars = set()

    def scan_items(items):
        for item in items:
            if "event" in item:
                for event in item["event"]:
                    if event.get("listen") == "test":
                        script_lines = event.get("script", {}).get("exec", [])
                        for line in script_lines:
                            matches = re.findall(
                                r"pm\.environment\.set\(['\"](.*?)['\"]", line
                            )
                            for var in matches:
                                chaining_vars.add(var)
            if "item" in item:
                scan_items(item["item"])

    scan_items(postman_collection["item"])
    return chaining_vars


def extract_env_variables(postman_collection):
    env_vars = set()

    def scan_text(text):
        matches = re.findall(r"{{(.*?)}}", text)
        for var in matches:
            env_vars.add(var)

    def scan_items(items):
        for item in items:
            if "request" in item:
                req = item["request"]
                if "raw" in req["url"]:
                    scan_text(req["url"]["raw"])
                if "header" in req:
                    for header in req["header"]:
                        scan_text(header["value"])
                if "body" in req:
                    body = req["body"]
                    if body["mode"] == "raw":
                        scan_text(body["raw"])
                    elif body["mode"] == "urlencoded":
                        for param in body["urlencoded"]:
                            scan_text(param["key"])
                            scan_text(param["value"])
            if "item" in item:
                scan_items(item["item"])

    scan_items(postman_collection["item"])
    return env_vars


def convert_variables(text, chaining_vars, env_vars):
    def replace_var(match):
        var_name = match.group(1).strip()
        if var_name in chaining_vars:
            return f"${{{var_name}}}"
        elif var_name in env_vars:
            return f"${{__ENV.{var_name}}}"
        else:
            return f"${{__ENV.{var_name}}}"

    return re.sub(r"{{\s*(.*?)\s*}}", replace_var, text)


def format_js_object(py_dict, chaining_vars, env_vars):
    parts = []
    for k, v in py_dict.items():
        if "{{" in v and "}}" in v:
            v_converted = convert_variables(v, chaining_vars, env_vars)
            parts.append(f"{json.dumps(k)}: `{v_converted}`")
        elif v.startswith("${__ENV") or v.startswith("${") or v.isdigit():
            parts.append(f"{json.dumps(k)}: `{v}`")
        else:
            parts.append(f"{json.dumps(k)}: {json.dumps(v)}")
    return "{" + ", ".join(parts) + "}"


def extract_all_requests(items):
    for item in items:
        if "request" in item:
            yield item
        elif "item" in item:
            yield from extract_all_requests(item["item"])


def generate_env_file(postman_environment):
    env_content = ""
    keys = set()
    for variable in postman_environment.get("values", []):
        if (
            variable.get("enabled", True)
            and variable.get("key")
            and variable.get("value") is not None
        ):
            key = str(variable["key"]).strip()
            value = str(variable["value"]).strip()
            env_content += f"{key}={value}\n"
            keys.add(key)
    return env_content, keys


def extract_chaining_variable_assignments(postman_collection):
    chaining_variable_assignments_per_api = {}

    def resolve_dependencies(var_name, assignments, visited=None):
        if visited is None:
            visited = []
        if var_name in visited:
            return []
        visited.append(var_name)
        expr = assignments.get(var_name)
        if not expr:
            return []
        deps = []
        tokens = re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b", expr)
        for token in tokens:
            if token in assignments:
                deps.extend(resolve_dependencies(token, assignments, visited))
        deps.append(var_name)
        return list(dict.fromkeys(deps))

    def scan_items(items):
        for item in items:
            api_name = item.get("name", "Unnamed")
            if "event" in item:
                for event in item["event"]:
                    if event.get("listen") == "test":
                        script_lines = event.get("script", {}).get("exec", [])
                        local_var_definitions = {}
                        for line in script_lines:
                            match_local = re.search(
                                r"(?:const|let|var)\s+(\w+)\s*=\s*(.*);", line
                            )
                            if match_local:
                                local_var_name = match_local.group(1)
                                local_var_expr = match_local.group(2).strip()
                                if "pm.response.json" in local_var_expr:
                                    local_var_expr = "RES_PLACEHOLDER.json()"
                                local_var_definitions[local_var_name] = local_var_expr
                        for line in script_lines:
                            match_env = re.search(
                                r"pm\.environment\.set\(['\"](.*?)['\"],\s*(.*)\);",
                                line,
                            )
                            if match_env:
                                env_var_name = match_env.group(1)
                                assignment_expr = match_env.group(2).strip().rstrip(";")
                                entry = {"assignment_expr": assignment_expr}
                                if assignment_expr in local_var_definitions:
                                    backtrack_chain = resolve_dependencies(
                                        assignment_expr, local_var_definitions
                                    )
                                    full_definitions = {
                                        var: local_var_definitions[var]
                                        for var in backtrack_chain
                                        if var in local_var_definitions
                                    }
                                    entry["local_var_definition"] = (
                                        local_var_definitions[assignment_expr]
                                    )
                                    entry["backtrack_chain"] = backtrack_chain
                                    entry["full_definitions"] = full_definitions
                                chaining_variable_assignments_per_api.setdefault(
                                    api_name, {}
                                )[env_var_name] = entry
            if "item" in item:
                scan_items(item["item"])

    scan_items(postman_collection["item"])
    return chaining_variable_assignments_per_api


def generate_k6_script(selected_apis, postman_collection):
    chaining_vars = extract_chaining_variables(postman_collection)
    env_vars = extract_env_variables(postman_collection)
    chaining_variable_assignments_per_api = extract_chaining_variable_assignments(
        postman_collection
    )

    k6_script = """
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend } from 'k6/metrics';
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';

export let options = {
    vus: 1,
    duration: '1s',
};
"""
    request_counter = 1
    trend_definitions = ""
    request_blocks = ""
    for api in selected_apis:
        trend_var = re.sub(r"\W+", "_", api["name"])
        sanitized_metric_name = re.sub(r"\W+", "_", api["name"])
        trend_definitions += (
            f"let {trend_var} = new Trend('{sanitized_metric_name}');\n"
        )
        for request in extract_all_requests(postman_collection["item"]):
            if request["name"] != api["name"]:
                continue
            method = request["request"]["method"]
            raw_url = convert_variables(
                request["request"]["url"]["raw"], chaining_vars, env_vars
            )
            headers = {
                h["key"]: h["value"]
                for h in request["request"].get("header", [])
                if "key" in h and "value" in h
            }
            url_var = f"url{request_counter}"
            block = f"\n  // {api['name']}\n"
            block += f"  let {url_var} = `{raw_url}`;\n"
            block += f"  let headers{request_counter} = {format_js_object(headers, chaining_vars, env_vars)};\n"
            if method == "GET":
                block += f"""
  let res{request_counter} = http.get({url_var}, {{ headers: headers{request_counter} }});
  console.log(`Request: GET ${{ {url_var} }}`);
  console.log('Response: ' + res{request_counter}.body);
  {trend_var}.add(res{request_counter}.timings.duration);
  check(res{request_counter}, {{
    'is status 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  }});\n"""
            elif method in ["POST", "PUT"]:
                payload = "{}"
                if "body" in request["request"]:
                    body = request["request"]["body"]
                    if body["mode"] == "raw":
                        payload = convert_variables(
                            body["raw"], chaining_vars, env_vars
                        )
                        headers["Content-Type"] = "application/json"
                    elif body["mode"] == "urlencoded":
                        payload = "&".join(
                            [
                                f"{item['key']}={convert_variables(item['value'], chaining_vars, env_vars)}"
                                for item in body["urlencoded"]
                            ]
                        )
                        headers["Content-Type"] = "application/x-www-form-urlencoded"
                payload_var = f"payload{request_counter}"
                block += f"""
  let {payload_var} = `{payload}`;
  let res{request_counter} = http.{method.lower()}({url_var}, {payload_var}, {{ headers: headers{request_counter} }});
  console.log(`Request: {method} ${{ {url_var} }}`);
  console.log(`Payload: ` + JSON.stringify({payload_var}));
  console.log(`Response: ` + res{request_counter}.body);
  {trend_var}.add(res{request_counter}.timings.duration);
  check(res{request_counter}, {{
    'is status 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  }});\n"""
            elif method == "DELETE":
                block += f"""
  let res{request_counter} = http.del({url_var}, null, {{ headers: headers{request_counter} }});
  console.log(`Request: DELETE ${{ {url_var} }}`);
  console.log('Response: ' + res{request_counter}.body);
  {trend_var}.add(res{request_counter}.timings.duration);
  check(res{request_counter}, {{
    'is status 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  }});\n"""
            if api["name"] in chaining_variable_assignments_per_api:
                chaining = chaining_variable_assignments_per_api[api["name"]]
                all_dependencies = {}
                ordered_vars = []
                for env_var, entry in chaining.items():
                    full_defs = entry.get("full_definitions", {})
                    backtrack = entry.get("backtrack_chain", [])
                    for var in backtrack:
                        if var not in all_dependencies:
                            all_dependencies[var] = full_defs.get(var)
                            ordered_vars.append(var)
                if ordered_vars or chaining:
                    block += f"  if (res{request_counter}.status === 200) {{\n"
                    block += f"    let jsonData = res{request_counter}.json();\n"
                    for var in ordered_vars:
                        expr = all_dependencies[var]
                        if expr:
                            expr = expr.replace(
                                "RES_PLACEHOLDER", f"res{request_counter}"
                            )
                            block += f"    let {var} = {expr};\n"
                    for env_var, entry in chaining.items():
                        expr = entry["assignment_expr"].replace(
                            "RES_PLACEHOLDER", f"res{request_counter}"
                        )
                        block += f"    let {env_var} = {expr};\n"
                    block += "  }\n"
            request_blocks += block
            request_counter += 1
    k6_script += "\n" + trend_definitions + "\n"
    declarations = (
        "  " + ";\n  ".join([f"let {var}" for var in chaining_vars]) + ";"
        if chaining_vars
        else ""
    )
    k6_script += "\nexport default function () {\n"
    k6_script += declarations + "\n"
    k6_script += request_blocks
    k6_script += "  sleep(1);\n}\n"
    k6_script += """
export function handleSummary(data) {
  return {
    "summary.html": htmlReport(data),
  };
}
"""
    return k6_script
