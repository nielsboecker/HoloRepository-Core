module.exports = {
  parser: "@typescript-eslint/parser", // Specifies the ESLint parser
  extends: [
    // Use the recommended rules from the @typescript-eslint/eslint-plugin
    "plugin:@typescript-eslint/recommended",
    // Use eslint-config-prettier to disable ESLint rules from @typescript-eslint/eslint-plugin that would conflict with prettier
    "prettier/@typescript-eslint"
    // Enable eslint-plugin-prettier and eslint-config-prettier. This will display prettier errors as ESLint errors.
    // Make sure this is always the last configuration in the extends array.
    // "plugin:prettier/recommended"
  ],
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: "module"
  },
  rules: {
    // Allow names like "IImagingStudy_Series"
    "@typescript-eslint/camelcase": 0,
    // Promise error handlers, Jest test cases etc. don't need explicit return type
    "@typescript-eslint/explicit-function-return-type": 0,
    // parseInt() may use default base of 10
    "radix": 0
  }
};