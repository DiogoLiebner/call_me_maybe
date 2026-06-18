import json
import math
import os
import re


def fn_add_numbers(a: int, b: int) -> int:
    return a + b


def fn_greet(name: str) -> str:
    return f"Hello, {name}!"


def fn_reverse_string(s: str) -> str:
    return s[::-1]


def fn_get_square_root(a: float) -> float:
    if a < 0:
        raise ValueError("Cannot compute square root of a negative number.")
    return math.sqrt(a)


def fn_substitute_string_with_regex(s: str, pattern: str, replacement: str) -> str:
    return re.sub(pattern, replacement, s)


def extract_json_call(text: str):
    """
    Extracts a JSON object from a string that contains a function
    call with a JSON argument.
    For example, if the input is 'fn_call({"key": "value"})',
    it will extract '{"key": "value"}'.
    """
    match = re.search(r'\((\{.*\})\)', text)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format.")
    else:
        raise ValueError("No JSON object found in the input string.")


SCHEMA = {
    "fn_add_numbers": {
        "args": {
            "a": int,
            "b": int
        }
    },
    "fn_greet": {
        "args": {
            "name": str
        }
    },
    "fn_reverse_string": {
        "args": {
            "s": str
        }
    },
    "fn_get_square_root": {
        "args": {
            "a": float
        }
    },
    "fn_substitute_string_with_regex": {
        "args": {
            "s": str,
            "pattern": str,
            "replacement": str
        }
    }
}


def validate_call(call: dict):
    name = call.get("name")
    args = call.get("args", {})

    if name not in SCHEMA:
        raise KeyError(f"Function '{name}' is not defined in the schema.")

    expected_args = SCHEMA[name]["args"]
    for arg_name, arg_type in expected_args.items():
        if arg_name not in args:
            raise ValueError(f"Missing argument '{arg_name}' \
for function '{name}'.")
        if not isinstance(args[arg_name], arg_type):
            raise TypeError(f"Argument '{arg_name}' must be \
of type {arg_type.__name__}.")


def dispatch_call(raw_llm_otuput: str):
    try:
        parsed = extract_json_call(raw_llm_otuput)
        calls = parsed if isinstance(parsed, list) else [parsed]
        results = []

        for call in calls:
            name, args = validate_call(call)
            result = REGISTRY[name](**args)
            results.append({"name": name, "args": args, "result": result})

        return results

    except (ValueError, KeyError, TypeError) as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
