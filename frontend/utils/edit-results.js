export const flattenResults = (result) => {
  const res = {};
  for (const key of Object.keys(result)) {
    const val = result[key];
    if (val["$oid"]) {
      res[key] = val["$oid"];
    } else if (val["$date"]) {
      res[key] = val["$date"];
    } else {
      res[key] = val;
    }
  }
  return res;
};
