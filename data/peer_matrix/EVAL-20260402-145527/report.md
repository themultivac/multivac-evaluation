# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-145527
**Timestamp:** 2026-04-02T14:55:27.892669
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

Implement a JSON Schema validator from scratch that supports: type validation (string, number, integer, boolean, array, object, null), required fields, minimum/maximum for numbers, minLength/maxLength for strings, pattern (regex), enum, nested objects, and array items validation. No external libraries.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | GPT-5.4 | 8.96 | 8.60 | 9.80 | 0.50 |
| 2 | DeepSeek V3 | 8.66 | 7.35 | 9.80 | 0.73 |
| 3 | Grok 4.20 | 8.61 | 7.75 | 9.80 | 0.65 |
| 4 | Gemini 3 Flash Preview | 8.20 | 7.00 | 8.80 | 0.59 |
| 5 | GPT-OSS-120B | 7.55 | 4.40 | 9.45 | 1.74 |
| 6 | MiMo-V2-Flash | 7.35 | 5.20 | 9.60 | 1.31 |
| 7 | Claude Sonnet 4.6 | 6.22 | 3.45 | 8.45 | 1.66 |
| 8 | Claude Opus 4.6 | 5.62 | 2.45 | 8.80 | 2.14 |
| 9 | MiniMax M2.5 | 3.59 | 0.20 | 7.00 | 2.20 |
| 10 | Gemini 3.1 Pro | 2.92 | 0.40 | 8.35 | 3.11 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 4.62 |
| 2 | Claude Opus 4.6 | 6.28 |
| 3 | GPT-OSS-120B | 6.38 |
| 4 | Grok 4.20 | 6.54 |
| 5 | Gemini 3.1 Pro | 6.74 |
| 6 | MiniMax M2.5 | 6.81 |
| 7 | Claude Sonnet 4.6 | 6.88 |
| 8 | MiMo-V2-Flash | 7.13 |
| 9 | Gemini 3 Flash Preview | 7.78 |
| 10 | DeepSeek V3 | 8.50 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** deepseek_v4
**Total Judgments:** 100
**Valid Judgments:** 90

---

## Model Pool

Models selected for **Code Generation** evaluation:

1. **GPT-5.4** (openrouter)
2. **Claude Opus 4.6** (openrouter)
3. **Gemini 3.1 Pro** (openrouter)
4. **Claude Sonnet 4.6** (openrouter)
5. **Grok 4.20** (openrouter)
6. **DeepSeek V3** (openrouter)
7. **GPT-OSS-120B** (openrouter)
8. **Gemini 3 Flash Preview** (openrouter)
9. **MiniMax M2.5** (openrouter)
10. **MiMo-V2-Flash** (openrouter)

---

## Model Responses

### GPT-5.4

**Generation Time:** 26118ms
**Tokens:** 2097

```
Below is a from-scratch JSON Schema validator in plain JavaScript with support for:

- `type`: `string`, `number`, `integer`, `boolean`, `array`, `object`, `null`
- `required`
- `minimum` / `maximum`
- `minLength` / `maxLength`
- `pattern`
- `enum`
- nested objects
- array `items` validation

No external libraries are used.

---

## Implementation

```js
class JSONSchemaValidator {
  validate(schema, data) {
    const errors = [];
    this._validateSchema(schema, data, '', errors);
    return {
      valid: errors.length === 0,
      errors
    };
  }

  _validateSchema(schema, data, path, errors) {
    if (!schema || typeof schema !== 'object') {
      errors.push({
        path,
        message: 'Invalid schema definition'
      });
      return;
    }

    // Type validation
    if (schema.type !== undefined) {
      if (!this._checkType(schema.type, data)) {
        errors.push({
          path,
          message: `Expected type ${schema.type} but got ${this._getType(data)}`
        });
        return; // stop deeper validation if type is wrong
      }
    }

    // Enum validation
    if (schema.enum !== undefined) {
      const found = schema.enum.some(value => this._deepEqual(value, data));
      if (!found) {
        errors.push({
          path,
          message: `Value must be one of: ${JSON.stringify(schema.enum)}`
        });
      }
    }

    // Type-specific validation
    switch (schema.type) {
      case 'number':
      case 'integer':
        this._validateNumber(schema, data, path, errors);
        break;

      case 'string':
        this._validateString(schema, data, path, errors);
        break;

      case 'object':
        this._validateObject(schema, data, path, errors);
        break;

      case 'array':
        this._validateArray(schema, data, path, errors);
        break;
    }
  }

  _validateNumber(schema, data, path, errors) {
    if (schema.minimum !== undefined && data < schema.minimum) {
      errors.push({
        path,
        ...
```

### Claude Opus 4.6

**Generation Time:** 195345ms
**Tokens:** 2118

```


# JSON Schema Validator from Scratch

```python
"""
A comprehensive JSON Schema validator implemented from scratch.
No external libraries used - only Python standard library.
"""

import re
import json
from typing import Any


class ValidationError:
    """Represents a single validation error with path context."""

    def __init__(self, message: str, path: str = ""):
        self.message = message
        self.path = path

    def __str__(self):
        if self.path:
            return f"At '{self.path}': {self.message}"
        return self.message

    def __repr__(self):
        return f"ValidationError({self!s})"

    def __eq__(self, other):
        if isinstance(other, ValidationError):
            return self.message == other.message and self.path == other.path
        return False


class ValidationResult:
    """Collects all validation errors for a given validation run."""

    def __init__(self):
        self.errors: list[ValidationError] = []

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(self, message: str, path: str = ""):
        self.errors.append(ValidationError(message, path))

    def merge(self, other: "ValidationResult"):
        self.errors.extend(other.errors)

    def __str__(self):
        if self.is_valid:
            return "Valid"
        lines = [f"Invalid - {len(self.errors)} error(s):"]
        for err in self.errors:
            lines.append(f"  - {err}")
        return "\n".join(lines)

    def __repr__(self):
        return f"ValidationResult(valid={self.is_valid}, errors={len(self.errors)})"


class JsonSchemaValidator:
    """
    JSON Schema validator supporting:
      - type validation (string, number, integer, boolean, array, object, null)
      - required fields
      - minimum / maximum / exclusiveMinimum / exclusiveMaximum for numbers
      - multipleOf for numbers
      - minLength / maxLength for strings
      - pattern (regex) for strings
      - enum
      - const
...
```

### Gemini 3.1 Pro

**Generation Time:** 31282ms
**Tokens:** 2105

```
Here is a complete, fully functional JSON Schema validator built from scratch in Python. It uses no external libraries (only the built-in `re` module for regex pattern matching).

It implements recursive validation to handle deeply nested objects and arrays, and collects all validation errors with their exact paths (e.g., `root.address.zipcode`) so you know exactly what failed.

### The Implementation

```
```

### Claude Sonnet 4.6

**Generation Time:** 25958ms
**Tokens:** 2118

```
# JSON Schema Validator from Scratch

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                  JSONSchemaValidator                  │
├─────────────────────────────────────────────────────┤
│  validate(data, schema) → ValidationResult           │
│  ├── TypeValidator                                   │
│  ├── StringValidator                                 │
│  ├── NumberValidator                                 │
│  ├── ArrayValidator                                  │
│  ├── ObjectValidator                                 │
│  └── CommonValidator (enum, required)                │
└─────────────────────────────────────────────────────┘
```

## Implementation

```javascript
// ============================================================
// Core Types & Utilities
// ============================================================

class ValidationError {
  constructor(path, message, value) {
    this.path = path;       // e.g., "user.address.zipCode"
    this.message = message;
    this.value = value;
  }

  toString() {
    return `[${this.path || 'root'}] ${this.message} (got: ${JSON.stringify(this.value)})`;
  }
}

class ValidationResult {
  constructor() {
    this.errors = [];
    this.valid = true;
  }

  addError(path, message, value) {
    this.errors.push(new ValidationError(path, message, value));
    this.valid = false;
  }

  merge(otherResult, pathPrefix = '') {
    for (const error of otherResult.errors) {
      const fullPath = pathPrefix
        ? error.path
          ? `${pathPrefix}.${error.path}`
          : pathPrefix
        : error.path;
      this.errors.push(new ValidationError(fullPath, error.message, error.value));
    }
    if (!otherResult.valid) this.valid = false;
  }

  toJSON() {
    return {
      valid: this.valid,
      errors: this.errors.map(e => ({
        path: e.path,
        message: e.message,
        value: e.value,
      })),
    };
  }
}

// ======================================...
```

### Grok 4.20

**Generation Time:** 12898ms
**Tokens:** 2035

```
**Here's a complete JSON Schema validator implemented from scratch in TypeScript:**

```typescript
type JsonValue = null | boolean | number | string | JsonValue[] | { [key: string]: JsonValue };

interface ValidationError {
  path: string;
  message: string;
}

interface Schema {
  type?: string | string[];
  required?: string[];
  properties?: { [key: string]: Schema };
  items?: Schema;
  minimum?: number;
  maximum?: number;
  minLength?: number;
  maxLength?: number;
  pattern?: string;
  enum?: JsonValue[];
  additionalProperties?: boolean | Schema;
  [key: string]: any;
}

export class JsonSchemaValidator {
  private errors: ValidationError[] = [];

  validate(data: JsonValue, schema: Schema, path: string = ''): ValidationError[] {
    this.errors = [];
    this._validate(data, schema, path);
    return this.errors;
  }

  private _validate(data: JsonValue, schema: Schema, path: string = ''): void {
    // Type validation
    if (schema.type) {
      this.validateType(data, schema.type, path);
    }

    // Required fields (for objects)
    if (schema.required && typeof data === 'object' && data !== null && !Array.isArray(data)) {
      this.validateRequired(data as Record<string, JsonValue>, schema.required, path);
    }

    // Object validation
    if (typeof data === 'object' && data !== null && !Array.isArray(data)) {
      if (schema.properties) {
        this.validateObject(data as Record<string, JsonValue>, schema, path);
      }
    }

    // Array validation
    if (Array.isArray(data) && schema.items) {
      this.validateArray(data, schema.items, path);
    }

    // Number validations
    if (typeof data === 'number') {
      this.validateNumber(data, schema, path);
    }

    // String validations
    if (typeof data === 'string') {
      this.validateString(data, schema, path);
    }

    // Enum validation
    if (schema.enum) {
      this.validateEnum(data, schema.enum, path);
    }
  }

  private validateType(data: JsonValue, type: string | s...
```

### DeepSeek V3

**Generation Time:** 130420ms
**Tokens:** 3031

```
# JSON Schema Validator Implementation

Here's a complete implementation of a JSON Schema validator from scratch in JavaScript that supports all the requested features:

```javascript
class SchemaValidator {
  constructor(schema) {
    this.schema = schema;
  }

  validate(data) {
    return this.validateAgainstSchema(data, this.schema);
  }

  validateAgainstSchema(data, schema, path = '') {
    if (schema === undefined) return true; // No schema means anything is valid
    
    // Handle $ref (not fully implemented as it wasn't in requirements)
    if (schema.$ref) {
      // In a real implementation, we'd resolve the reference
      throw new Error('$ref references are not supported in this implementation');
    }

    // Validate type
    if (schema.type && !this.validateType(data, schema.type)) {
      return this.fail(`Expected type ${schema.type} but got ${typeof data}`, path);
    }

    // Validate const (exact value match)
    if ('const' in schema && data !== schema.const) {
      return this.fail(`Value must be exactly ${JSON.stringify(schema.const)}`, path);
    }

    // Validate enum
    if (schema.enum && !schema.enum.includes(data)) {
      return this.fail(`Value must be one of: ${schema.enum.join(', ')}`, path);
    }

    // Validate null specifically (since typeof null === 'object')
    if (schema.type === 'null' && data !== null) {
      return this.fail(`Value must be null`, path);
    }

    // Object-specific validations
    if (typeof data === 'object' && data !== null && !Array.isArray(data)) {
      return this.validateObject(data, schema, path);
    }

    // Array-specific validations
    if (Array.isArray(data)) {
      return this.validateArray(data, schema, path);
    }

    // String-specific validations
    if (typeof data === 'string') {
      return this.validateString(data, schema, path);
    }

    // Number-specific validations
    if (typeof data === 'number') {
      return this.validateNumber(data, schema, path);
    }

   ...
```

### GPT-OSS-120B

**Generation Time:** 19442ms
**Tokens:** 2181

```
Below is a **self‑contained** JSON‑Schema validator written in pure Python (standard library only).  
It supports the features you asked for:

| Feature | JSON‑Schema keyword | Implementation |
|---------|--------------------|----------------|
| **Type validation** | `type` (`string`, `number`, `integer`, `boolean`, `array`, `object`, `null`) | Python type mapping |
| **Required fields** | `required` (array of property names) | Checked for objects |
| **Numeric limits** | `minimum`, `maximum` | Applied to `number`/`integer` |
| **String limits** | `minLength`, `maxLength`, `pattern` | Length checks + `re.fullmatch` |
| **Enum** | `enum` (array of allowed values) | Direct value comparison |
| **Nested objects** | `properties` (object) + recursion | Recursive validation |
| **Array items** | `items` (schema) | Each element validated against the same schema |

The validator returns **all** errors it can find (instead of stopping at the first one) and tells you exactly where in the document the problem is (`path`).

---  

## 1️⃣  The validator implementation

```python
import re
from typing import Any, Dict, List, Tuple, Union

JSONSchema = Dict[str, Any]          # a tiny alias to make signatures clearer
ValidationError = Tuple[str, str]    # (path, message)


class JSONSchemaValidator:
    """
    Minimal JSON‑Schema validator (draft‑07 subset).

    Usage
    -----
    >>> validator = JSONSchemaValidator()
    >>> errors = validator.validate(data, schema)
    >>> if errors:
    ...     for path, msg in errors:
    ...         print(f"{path}: {msg}")
    """

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def validate(self, data: Any, schema: JSONSchema) -> List[ValidationError]:
        """
        Validate *data* against *schema*.

        Returns a list of `(path, message)` tuples.
        An empty list means the data is valid.
        ...
```

### Gemini 3 Flash Preview

**Generation Time:** 15350ms
**Tokens:** 1690

```
This implementation provides a core JSON Schema validator engine. It recursively traverses the schema and the data, collecting all validation errors found.

### The Validator Implementation

```javascript
class JsonSchemaValidator {
    constructor() {
        this.errors = [];
    }

    validate(schema, data, path = "") {
        // Reset errors on root call
        if (path === "") this.errors = [];

        if (!schema) return true;

        this._validateType(schema, data, path);
        this._validateEnum(schema, data, path);

        // Type-specific validations
        const type = schema.type;
        if (type === 'number' || type === 'integer') {
            this._validateNumeric(schema, data, path);
        } else if (type === 'string') {
            this._validateString(schema, data, path);
        } else if (type === 'object') {
            this._validateObject(schema, data, path);
        } else if (type === 'array') {
            this._validateArray(schema, data, path);
        }

        return {
            valid: this.errors.length === 0,
            errors: this.errors
        };
    }

    _addError(message, path) {
        this.errors.push({ path: path || "root", message });
    }

    _validateType(schema, data, path) {
        const type = schema.type;
        if (!type) return;

        const actualType = data === null ? 'null' : Array.isArray(data) ? 'array' : typeof data;
        
        let isValid = false;
        if (type === 'integer') {
            isValid = Number.isInteger(data);
        } else if (type === 'number') {
            isValid = typeof data === 'number';
        } else {
            isValid = actualType === type;
        }

        if (!isValid) {
            this._addError(`Expected type ${type} but got ${actualType}`, path);
        }
    }

    _validateEnum(schema, data, path) {
        if (schema.enum && !schema.enum.includes(data)) {
            this._addError(`Value must be one of: [${schema.enum.join(", ")}]`, pa...
```

### MiniMax M2.5

**Generation Time:** 10258ms
**Tokens:** 2147

```
Here is a complete, standalone JSON Schema validator implemented in JavaScript without any external libraries.

It handles all the requested features: types, required fields, numeric constraints, string constraints, regex patterns, enums, nested objects, and array validation.

### The Implementation

```javascript
/**
 * Validates data against a JSON Schema.
 * @param {any} data - The data to validate.
 * @param {object} schema - The JSON Schema to validate against.
 * @param {string} [path='root'] - Current path for error reporting.
 * @returns {object} - { valid: boolean, errors: array }
 */
function validate(data, schema, path = 'root') {
    const errors = [];

    // Helper to add an error
    const addError = (message) => {
        errors.push({ path, message });
    };

    // 1. TYPE VALIDATION
    if (schema.type) {
        let actualType = typeof data;

        // Normalize types
        if (data === null) actualType = 'null';
        else if (Array.isArray(data)) actualType = 'array';

        // Handle schema.type being a single string or an array of strings
        const allowedTypes = Array.isArray(schema.type) ? schema.type : [schema.type];

        // Specific check for integer (since typeof returns 'number')
        let typeMatch = allowedTypes.includes(actualType);
        if (actualType === 'number' && allowedTypes.includes('integer')) {
            if (Number.isInteger(data)) typeMatch = true;
        }

        if (!typeMatch) {
            addError(`Expected type '${schema.type}', got '${actualType}'`);
            // If type fails, we often stop validating specific constraints for this node,
            // but we continue to check structural things like 'required' if it's an object.
        }
    }

    // Stop further validation if type is fundamentally wrong (e.g. expecting object, got string)
    // However, we allow validation to continue for specific cases like 'null' vs 'object'.
    const isObject = typeof data === 'object' && data !== ...
```

### MiMo-V2-Flash

**Generation Time:** 22939ms
**Tokens:** 2145

```
Here is a complete, single-file implementation of a JSON Schema validator in Python.

It handles all the requirements: type checking, required fields, numeric constraints, string constraints (min/max length, regex), enums, nested objects, and array items (both homogeneous and tuple validation).

### The Validator Code

```python
import re
import json

class SchemaValidationError(Exception):
    """Custom exception to hold validation errors."""
    def __init__(self, message, path=""):
        self.message = message
        self.path = path
        super().__init__(self.__str__())

    def __str__(self):
        return f"Validation Error at '{self.path}': {self.message}"

class JSONSchemaValidator:
    """
    A from-scratch JSON Schema validator supporting:
    - type: string, number, integer, boolean, array, object, null
    - required fields
    - minimum, maximum (exclusiveMinimum, exclusiveMaximum optional)
    - minLength, maxLength
    - pattern (regex)
    - enum
    - nested objects (properties, additionalProperties)
    - array items validation (items schema or tuple validation)
    """

    def __init__(self, schema):
        self.schema = schema

    def validate(self, data):
        """
        Validates the provided data against the schema.
        Returns True if valid.
        Raises SchemaValidationError if invalid.
        """
        try:
            self._validate_node(self.schema, data, "$")
            return True
        except SchemaValidationError as e:
            raise e

    def _validate_node(self, schema, data, path):
        """
        Recursive validation function.
        schema: The JSON schema object for the current node.
        data: The actual data to validate.
        path: JSON pointer path for error reporting (e.g., $.user.address).
        """
        # 1. Handle 'type' validation
        if "type" in schema:
            expected_type = schema["type"]
            
            # Normalize Python types to JSON types
          ...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*