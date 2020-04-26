'use strict'
let assert = require('assert')
let spyOnComponent = require('./')

let staticCalled = false
let staticInnerCalled = false
let innerCalled = false
let called = false

function foo() {
  innerCalled = true
}

class Component {
  static getDerivedStateFromProps() {
    staticInnerCalled = true
  }
}

Component.prototype.componentWillMount = foo
const component = new Component()

let reset = spyOnComponent(component, {
  getDerivedStateFromProps() {
    staticCalled = true
  },
  componentWillMount() {
    called = true
  },
  componentDidMount: foo,
})

assert(true, 'it didnt have runtime errors')
//
//
;((/* it should wrap methods */) => {
  component.componentWillMount()

  assert(called)
  assert(innerCalled)
})()
//
//
;((/* it should wrap static methods */) => {
  Component.getDerivedStateFromProps()

  assert(staticCalled)
  assert(staticInnerCalled)
})()
//
//
;((/* it should only wrap when needed */) => {
  assert.equal(component.componentDidMount, foo)
})()
//
//
;((/* it should reset by key */) => {
  reset('componentDidMount')

  assert.equal(component.componentDidMount, undefined)
  assert.notEqual(component.componentWillMount, foo)
})()
//
//
;((/* it should reset */) => {
  reset()
  assert.equal(component.componentWillMount, foo)
})()
