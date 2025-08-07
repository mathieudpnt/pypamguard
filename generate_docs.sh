#!/bin/bash
set -euo pipefail

# Ensure VERSION is set
if [[ -z "${VERSION:-}" ]]; then
  echo "Error: VERSION environment variable is not set."
  exit 1
fi

# Generate documentation
pdoc -o temp_docs src/pypamguard

# Replace {{ version }} placeholder in all HTML files
find temp_docs -name "*.html" -exec sed -i "s/{{ version }}/$VERSION/g" {} +

# Move docs to versioned subfolder
rm -rf docs
mkdir -p docs/"$VERSION"
mv temp_docs/* docs/"$VERSION"

# Create redirect index.html to latest version
cat > docs/index.html <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Redirecting to latest version</title>
    <script>
        window.location.replace("./$VERSION/");
    </script>
</head>
<body>
    <p>If you are not redirected, click <a href="./$VERSION/">here</a>.</p>
</body>
</html>
EOF
