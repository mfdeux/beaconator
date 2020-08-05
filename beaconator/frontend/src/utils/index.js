import isEqual from 'lodash.isequal';

/*
Diff object, returning only changed fields
*/
export const objDiff = (oldObj, newObj) => {
  const returnedObj = {};
  const changedKeys = Object.keys(newObj).filter((k) => !isEqual(oldObj[k], newObj[k]));
  changedKeys.forEach((k) => (returnedObj[k] = newObj[k]));
  return returnedObj;
};
