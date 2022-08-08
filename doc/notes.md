
- Each decorator must know its level
  - Typically a type-level decorator is at level 0
  - An inner decorator (eg constraint) is at level 1
  - ...

- Decorator execution comes at the end of its level. So,
  execution of a type-level decorator happens once all the
  inner decorators have been evaluated

- Assume that category-speific type data is stored in '_typedata'
- Assume that category-specific instance data is stored in '_instdata'

- This is specialized for cases 