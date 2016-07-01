import { createStore } from 'redux';

// the function T(state, action) => state'
// the 'reducer'

const counter = (state = 0, action) => {
  switch (action.type) {
    case 'INCREMENT':
      return state + 1;
    // more cases here
    default:
      return state;
  }
}

// wiring together subscribe(), getState(), render(), dispatch()

const store = createStore(counter);

const render = () => {
  document.body.innerText = store.getState();
}

store.subscribe(render);

document.addEventListener('click', () => {
  store.dispatch({ type: 'INCREMENT' });
});

// implementing createStore

const createStore = (reducer) => {
  let state;
  let listeners = [];

  const getState = () => state;

  const dispatch = (action) => {
    // F(state, action) => 'state
    state = reducer(state, action);
    // subscribe callback
    listeners.forEach(listener => listener());
  };

  const subscribe = (listener) => {
    listeners.push(listener);
    // return unsubscribe function (removes from listener array)
    return () => {
      listeners = listeners.filter(l => l !== listener);
    };
  };

  // call reducer with dummy action to return initial state
  dispatch({});

  return { getState, dispatch, subscribe };
};

// example of editing just one counter in a list of counters, assuming this is
// all immutable

const incrementCounter = (list, index) => {
  return list
    .slice(0, index)
    .concat([list[index] + 1])
    .concat(list.slice(index + 1));
};

