import json
import re
import os
import time
import subprocess
import argparse
from datetime import datetime

def list_apis(postman_collection):
    apis = []
    
    def extract_requests(items):
        for item in items:
            if 'request' in item:
                apis.append({
                    'name': item['name'],
                    'method': item['request']['method'],
                    'url': item['request']['url']['raw']
                })
            elif 'item' in item:
                extract_requests(item['item'])
                
    extract_requests(postman_collection['item'])
    return apis

def extract_chaining_variables(postman_collection):
    chaining_vars = set()
    
    def scan_items(items):
        for item in items:
            if 'event' in item:
                for event in item['event']:
                    if event.get('listen') == 'test':
                        script_lines = event.get('script', {}).get('exec', [])
                        for line in script_lines:
                            matches = re.findall(r"pm\.environment\.set\(['\"](.*?)['\"]", line)
                            for var in matches:
                                print(f"DEBUG: found chaining variable via pm.environment.set: {var}")
                                chaining_vars.add(var)
            if 'item' in item:
                scan_items(item['item'])
                
    scan_items(postman_collection['item'])
    print(f"DEBUG: total chaining variables identified: {chaining_vars}")
    return chaining_vars

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
        # Find variable tokens in the expression
        tokens = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', expr)
        for token in tokens:
            if token in assignments:
                deps.extend(resolve_dependencies(token, assignments, visited))
        deps.append(var_name)
        return list(dict.fromkeys(deps))  # remove duplicates, preserve order

    def scan_items(items):
        for item in items:
            api_name = item.get('name', 'Unnamed')
            if 'event' in item:
                for event in item['event']:
                    if event.get('listen') == 'test':
                        script_lines = event.get('script', {}).get('exec', [])
                        local_var_definitions = {}

                        # Step 1: Collect all assignments
                        for line in script_lines:
                            match_local = re.search(r"(?:const|let|var)\s+(\w+)\s*=\s*(.*);", line)
                            if match_local:
                                local_var_name = match_local.group(1)
                                local_var_expr = match_local.group(2).strip()

                                # Special case: pm.response.json()
                                if "pm.response.json" in local_var_expr:
                                    local_var_expr = "RES_PLACEHOLDER.json()"

                                local_var_definitions[local_var_name] = local_var_expr
                                print(f"DEBUG: API '{api_name}' → local var '{local_var_name}' = {local_var_expr}")

                        # Step 2: Look for env.set calls
                        for line in script_lines:
                            match_env = re.search(r"pm\.environment\.set\(['\"](.*?)['\"],\s*(.*)\);", line)
                            if match_env:
                                env_var_name = match_env.group(1)
                                assignment_expr = match_env.group(2).strip().rstrip(";")

                                print(f"DEBUG: API '{api_name}' → env var '{env_var_name}' ← {assignment_expr}")

                                entry = {
                                    "assignment_expr": assignment_expr
                                }

                                # If the assignment is a variable, backtrack
                                if assignment_expr in local_var_definitions:
                                    backtrack_chain = resolve_dependencies(assignment_expr, local_var_definitions)

                                    full_definitions = {
                                        var: local_var_definitions[var]
                                        for var in backtrack_chain
                                        if var in local_var_definitions
                                    }

                                    entry["local_var_definition"] = local_var_definitions[assignment_expr]
                                    entry["backtrack_chain"] = backtrack_chain
                                    entry["full_definitions"] = full_definitions

                                    print(f"DEBUG: Backtrack for '{env_var_name}' → {backtrack_chain}")

                                chaining_variable_assignments_per_api.setdefault(api_name, {})[env_var_name] = entry

            if 'item' in item:
                scan_items(item['item'])

    scan_items(postman_collection['item'])
    print(f"DEBUG: Final chaining map: {chaining_variable_assignments_per_api}")
    return chaining_variable_assignments_per_api

def extract_env_variables(postman_collection):
    env_vars = set()

    def scan_text(text):
        matches = re.findall(r"{{(.*?)}}", text)
        for var in matches:
            env_vars.add(var)

    def scan_items(items):
        for item in items:
            if 'request' in item:
                req = item['request']

                # URL
                if 'raw' in req['url']:
                    scan_text(req['url']['raw'])

                # Headers
                if 'header' in req:
                    for header in req['header']:
                        scan_text(header['value'])

                # Body
                if 'body' in req:
                    body = req['body']
                    if body['mode'] == 'raw':
                        scan_text(body['raw'])
                    elif body['mode'] == 'urlencoded':
                        for param in body['urlencoded']:
                            scan_text(param['key'])
                            scan_text(param['value'])

            if 'item' in item:
                scan_items(item['item'])

    scan_items(postman_collection['item'])
    print(f"DEBUG: total env variables identified: {env_vars}")
    return env_vars

def convert_variables(text, chaining_vars, env_vars):
    def replace_var(match):
        var_name = match.group(1).strip()
        if var_name in chaining_vars:
            print(f"DEBUG: Treating variable '{var_name}' as chaining → ${{{var_name}}}")
            return f"${{{var_name}}}"
        elif var_name in env_vars:
            print(f"DEBUG: Treating variable '{var_name}' as env → ${{__ENV.{var_name}}}")
            return f"${{__ENV.{var_name}}}"
        else:
            print(f"WARNING: Variable '{var_name}' not found → fallback to env → ${{__ENV.{var_name}}}")
            return f"${{__ENV.{var_name}}}"

    return re.sub(r"{{\s*(.*?)\s*}}", replace_var, text)

def format_js_object(py_dict, chaining_vars, env_vars):
    print("DEBUG: Formatting JS object from:", py_dict)
    parts = []

    for k, v in py_dict.items():
        # Case: Variable template inside string, like "Bearer {{accessToken}}"
        if '{{' in v and '}}' in v:
            v_converted = convert_variables(v, chaining_vars, env_vars)
            parts.append(f"{json.dumps(k)}: `{v_converted}`")

        # Case: already a JS variable template like ${...} or digit string
        elif v.startswith('${__ENV') or v.startswith('${') or v.isdigit():
            parts.append(f"{json.dumps(k)}: `{v}`")

        # Case: plain static string
        else:
            parts.append(f"{json.dumps(k)}: {json.dumps(v)}")

    result = '{' + ', '.join(parts) + '}'
    print(f"DEBUG: final formatted js object: {result}")
    return result

def extract_all_requests(items):
    for item in items:
        if 'request' in item:
            print(f"DEBUG: found request: {item['name']}")
            yield item
        elif 'item' in item:
            print(f"DEBUG: Entering nested item: {item.get('name', 'Unnamed')}")
            yield from extract_all_requests(item['item'])

#Hybrid
def generate_k6_script(selected_apis, postman_collection):
    chaining_vars = extract_chaining_variables(postman_collection)
    env_vars = extract_env_variables(postman_collection)
    chaining_variable_assignments_per_api = extract_chaining_variable_assignments(postman_collection)

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
        trend_var = re.sub(r'\W+', '_', api['name'])
        sanitized_metric_name = re.sub(r'\W+', '_', api['name'])
        trend_definitions += f"let {trend_var} = new Trend('{sanitized_metric_name}');\n"

        for request in extract_all_requests(postman_collection['item']):
            if request['name'] != api['name']:
                continue

            method = request['request']['method']
            raw_url = convert_variables(request['request']['url']['raw'], chaining_vars, env_vars)

            # Deduplicate headers
            headers = {
                h['key']: h['value']
                for h in request['request'].get('header', [])
                if 'key' in h and 'value' in h
            }

            url_var = f"url{request_counter}"
            block = f"\n  // {api['name']}\n"
            block += f"  let {url_var} = `{raw_url}`;\n"
            block += f"  let headers{request_counter} = {format_js_object(headers, chaining_vars, env_vars)};\n"

            if method == 'GET':
                block += f"""
  let res{request_counter} = http.get({url_var}, {{ headers: headers{request_counter} }});
  console.log(`Request: GET ${{ {url_var} }}`);
  console.log('Response: ' + res{request_counter}.body);
  {trend_var}.add(res{request_counter}.timings.duration);
  check(res{request_counter}, {{
    'is status 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  }});\n"""

            elif method in ['POST', 'PUT']:
                payload = "{}"
                if 'body' in request['request']:
                    body = request['request']['body']
                    if body['mode'] == 'raw':
                        payload = convert_variables(body['raw'], chaining_vars, env_vars)
                        headers['Content-Type'] = 'application/json'
                    elif body['mode'] == 'urlencoded':
                        payload = '&'.join([
                            f"{item['key']}={convert_variables(item['value'], chaining_vars, env_vars)}"
                            for item in body['urlencoded']
                        ])
                        headers['Content-Type'] = 'application/x-www-form-urlencoded'

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

            elif method == 'DELETE':
                block += f"""
  let res{request_counter} = http.del({url_var}, null, {{ headers: headers{request_counter} }});
  console.log(`Request: DELETE ${{ {url_var} }}`);
  console.log('Response: ' + res{request_counter}.body);
  {trend_var}.add(res{request_counter}.timings.duration);
  check(res{request_counter}, {{
    'is status 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  }});\n"""

            # Chaining logic injection
            if api['name'] in chaining_variable_assignments_per_api:
                chaining = chaining_variable_assignments_per_api[api['name']]
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
                            expr = expr.replace("RES_PLACEHOLDER", f"res{request_counter}")
                            if var in chaining_vars:
                                # global chained var – already declared at top
                                block += f"    {var} = {expr};\n"
                            else:
								# intermediate helper var like `response`, `lastSlashIndex`
                                block += f"    let {var} = {expr};\n"

                    for env_var, entry in chaining.items():
                        expr = entry['assignment_expr'].replace("RES_PLACEHOLDER", f"res{request_counter}")
                        if env_var in chaining_vars:
                            block += f"    {env_var} = {expr};\n"
                        else:
                            block += f"    let {env_var} = {expr};\n"

                    block += "  }\n"

            request_blocks += block
            request_counter += 1

    # Final assembly
    k6_script += "\n" + trend_definitions + "\n"

    if chaining_vars:
        declarations = "  " + ";\n  ".join([f"let {var}" for var in chaining_vars]) + ";"
    else:
        declarations = ""

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

def generate_env_file(postman_environment):
    env_content = ""
    keys = set()
    
    for variable in postman_environment.get('values', []):
        if variable.get("enabled", True) and variable.get("key") and variable.get("value") is not None:
            key = str(variable['key']).strip()
            value = str(variable['value']).strip()
            env_content += f"{key}={value}\n"
            keys.add(key)

    return env_content, keys

def main():
    parser = argparse.ArgumentParser(description="Convert Postman collection to k6 script.")
    parser.add_argument('--collection', required=True, help='Path to the Postman collection JSON file')
    parser.add_argument('--env', help='Path to the Postman environment file (optional)')
    parser.add_argument('--all', action='store_true', help='Include all APIs in the collection')
    parser.add_argument('--include', help='Comma-separated list of API indices to include (e.g. 1,3,5)')

    args = parser.parse_args()

    try:
        with open(args.collection, 'r', encoding='utf-8') as file:
            postman_collection = json.load(file)
        print("✅ Postman collection loaded.")
    except Exception as e:
        print(f"❌ Error loading collection: {e}")
        return

    if args.env:
        try:
            with open(args.env, 'r', encoding='utf-8') as file:
                postman_environment = json.load(file)
            print("✅ Environment file loaded.")
            env_content, keys = generate_env_file(postman_environment)
            with open('.env', 'w', encoding='utf-8') as file:
                file.write(env_content)
            print(".env file generated.")
            if 'proxyURL' not in keys:
                print("▲ Warning: 'proxyURL' not found in the environment file.")
        except Exception as e:
            print(f"❌ Error loading environment file: {e}")
            return

    apis = list_apis(postman_collection)
    print(f"\n📦 Found {len(apis)} APIs in the collection.")

    if args.all:
        selected_apis = apis
        print("✅ --all flag set: All APIs included.")

    elif args.include:
        try:
            selected_indices = [int(i.strip()) - 1 for i in args.include.split(',')]
            selected_apis = [apis[i] for i in selected_indices]
            print(f"✅ --include flag set: APIs {args.include} selected.")
        except Exception as e:
            print(f"❌ Invalid --include input: {e}")
            return

    else:
        print("\nAvailable APIs:")
        for idx, api in enumerate(apis):
            print(f"[{idx + 1}]. {api['name']}  ({api['method']}  {api['url']})")
        selected_indices_input = input("\nEnter the indices of the APIs to include (comma-separated): ")
        selected_indices = [int(idx.strip()) - 1 for idx in selected_indices_input.split(',')]
        selected_apis = [apis[idx] for idx in selected_indices]

    k6_script = generate_k6_script(selected_apis, postman_collection)

    collection_name = os.path.splitext(os.path.basename(args.collection))[0].replace(' ', '')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    timezone_abbr = time.strftime("%Z")
    k6_filename = f"{collection_name}_{timestamp}_{timezone_abbr}_k6_script.js"

    with open(k6_filename, 'w', encoding='utf-8') as file:
        file.write(k6_script)

    print(f"\n🎯 K6 script saved as: {k6_filename}")
if __name__ == "__main__":
    main()
