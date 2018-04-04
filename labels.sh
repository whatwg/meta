echo ""
echo "Setup a repository with WHATWG labels"

echo ""
echo -n "GitHub personal access tokens: "
read -s TOKEN

echo ""
echo -n "GitHub repository (e.g., foo/bar): "
read REPO

REPO_USER=$(echo "$REPO" | cut -f1 -d /)
REPO_NAME=$(echo "$REPO" | cut -f2 -d /)

delete_label() {
  curl -u $TOKEN:x-oauth-basic --request DELETE "https://api.github.com/repos/$REPO_USER/$REPO_NAME/labels/$1"
}

add_label() {
  curl -u $TOKEN:x-oauth-basic --include --request POST --data "{\"name\": \"$1\", \"color\": \"$2\"}" "https://api.github.com/repos/$REPO_USER/$REPO_NAME/labels"
}

# Delete labels (note that spaces need to be encoded here)
for LABEL in "bug" "duplicate" "enhancement" "help%20wanted" "invalid" "question" "wontfix"
  do
    delete_label "$LABEL"
  done

# Create labels (note that spaces are not encoded here)
# (Does not include "good first issue" as it's a default.)
for LABEL in "addition/proposal|d4c5f9" \
             "clarification|fef2c0" \
             "compat|bfd4f2" \
             "do not merge yet|e11d21" \
             "i18n-comment|d4c5f9" \
             "i18n-tracking|d4c5f9" \
             "interop|c5def5" \
             "needs concrete proposal|1cddc7" \
             "needs implementer interest|5319e7" \
             "needs tests|b60205" \
             "removal/deprecation|eb6420" \
             "security/privacy|0052cc" \
             "topic: custom elements|009800" \
             "topic: shadow|009800"
  do
    LABEL_NAME=$(echo "$LABEL" | cut -f1 -d "|")
    LABEL_COLOR=$(echo "$LABEL" | cut -f2 -d "|")
    add_label "$LABEL_NAME" "$LABEL_COLOR"
  done
