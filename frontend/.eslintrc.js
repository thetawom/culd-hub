module.exports = {
    root: true,
    extends: ["eslint:recommended", "plugin:react/recommended"],
    env: {
        browser: true,
        node: true,
        es2021: true,
    },
    parserOptions: {
        ecmaFeatures: {
            jsx: true,
        },
        sourceType: "module",
    },
    overrides: [
        {
            files: ["**/*.ts", "**/*.tsx"],
            plugins: [
                "@typescript-eslint",
            ],
            extends: ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
            parser: "@typescript-eslint/parser",
            parserOptions: {
                project: ["./tsconfig.json"],
            },
        },
    ],
    settings: {
        react: {
            version: "detect"
        }
    },
    rules: {
        quotes: [1, "double"]
    }
};