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
`contextTypes` allows you to require a certain context like propTypes

### render props

A pattern where a container-like component is passed a function that it then
calls in its render method. This way you can pass a bunch of different low-state
components in. It's a lot like a HOC / mixin.

```
class ComponentWithState extends React.Component {
  state = {
    foo: 'hello',
  }

  render() {
    const { render } = this.props
    return (
      {render(this.state)}
    )
  }
}

class DisplayFoo extends React.Component {
  render() {
    const { foo } = this.props
    return (
      <h1>{foo}</h1>
    )
  }
}

function App() {
  return <ComponentWithState render={fooState => <DisplayFoo foo={fooState} />} />
}
