/**
 * Lo-Dash 2.2.1 (Custom Build) <http://lodash.com/>
 * Build: `lodash modularize modern exports="amd" -o ./modern/`
 * Copyright 2012-2013 The Dojo Foundation <http://dojofoundation.org/>
 * Based on Underscore.js 1.5.2 <http://underscorejs.org/LICENSE>
 * Copyright 2009-2013 Jeremy Ashkenas, DocumentCloud and Investigative Reporters & Editors
 * Available under MIT license <http://lodash.com/license>
 */
define(['../internals/baseCreateCallback', '../internals/createObject', '../collections/forEach', './forOwn', './isArray'], function(baseCreateCallback, createObject, forEach, forOwn, isArray) {

  /**
   * An alternative to `_.reduce` this method transforms `object` to a new
   * `accumulator` object which is the result of running each of its elements
   * through a callback, with each callback execution potentially mutating
   * the `accumulator` object. The callback is bound to `thisArg` and invoked
   * with four arguments; (accumulator, value, key, object). Callbacks may exit
   * iteration early by explicitly returning `false`.
   *
   * @static
   * @memberOf _
   * @category Objects
   * @param {Array|Object} collection The collection to iterate over.
   * @param {Function} [callback=identity] The function called per iteration.
   * @param {*} [accumulator] The custom accumulator value.
   * @param {*} [thisArg] The `this` binding of `callback`.
   * @returns {*} Returns the accumulated value.
   * @example
   *
   * var squares = _.transform([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], function(result, num) {
   *   num *= num;
   *   if (num % 2) {
   *     return result.push(num) < 3;
   *   }
   * });
   * // => [1, 9, 25]
   *
   * var mapped = _.transform({ 'a': 1, 'b': 2, 'c': 3 }, function(result, num, key) {
   *   result[key] = num * 3;
   * });
   * // => { 'a': 3, 'b': 6, 'c': 9 }
   */
  function transform(object, callback, accumulator, thisArg) {
    var isArr = isArray(object);
    callback = baseCreateCallback(callback, thisArg, 4);

    if (accumulator == null) {
      if (isArr) {
        accumulator = [];
      } else {
        var ctor = object && object.constructor,
            proto = ctor && ctor.prototype;

        accumulator = createObject(proto);
      }
    }
    (isArr ? forEach : forOwn)(object, function(value, index, object) {
      return callback(accumulator, value, index, object);
    });
    return accumulator;
  }

  return transform;
});
