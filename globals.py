import streamlit as st

def load_global_styles(css_file: str = "globals.css"):
    with open(css_file, "r") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

primaryColor = "#2E7D32"
backgroundColor = "#F8F9FA"
textColor = "#2E2E2E"
borderColor = "#D0E9D4"
linkColor = "#388E3C"
buttonBgColor = "#A1E7A7"
buttonHoverColor = "#3ECC4D"
buttonBorderColor = "#72D87B"

ACE_LANG_OPTIONS = {
    "Python": {
        "mode": "python",
        "extension": "py",
        "placeholder": "def placeholder():\n    print('Hello World')"
    },
    "JavaScript": {
        "mode": "javascript",
        "extension": "js",
        "placeholder": "function placeholder() {\n    console.log('Hello World');\n}"
    },
    "C++": {
        "mode": "c_cpp",
        "extension": "cpp",
        "placeholder": "#include<iostream>\nint main() {\n    std::cout << \"Hello World\";\n    return 0;\n}"
    },
    "Java": {
        "mode": "java",
        "extension": "java",
        "placeholder": "public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println(\"Hello World\");\n    }\n}"
    },
    "Go": {
        "mode": "golang",
        "extension": "go",
        "placeholder": "package main\nimport \"fmt\"\nfunc main() {\n    fmt.Println(\"Hello World\")\n}"
    },
    "PHP": {
        "mode": "php",
        "extension": "php",
        "placeholder": "<?php\necho 'Hello World';\n?>"
    },
    "Swift": {
        "mode": "swift",
        "extension": "swift",
        "placeholder": "print(\"Hello World\")"
    },
    "TypeScript": {
        "mode": "typescript",
        "extension": "ts",
        "placeholder": "function placeholder(): void {\n    console.log('Hello World');\n}"
    },
}