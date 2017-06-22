# React Notes

### Stateless Functional Components
These make sense because the React view hierarchy is a composition of a number
of functions.  A React component is "functional" in its render method.
Stateless Functional Components make this more obvious.

```
var ProfilePic = function(props){
  return <div>{this.props.foo}</div>;
}
```

__What's a 'Pure Function'?__

- Always return same result given same arguments
- Doesn't depend on state of application
- Don't modify state outside of their scope

FIRST: Focused Independent Reusable Small Testable

### Context

Context allows you pass data down the hierarchy without using props.
`contextTypes` allows you to require a certain context.

