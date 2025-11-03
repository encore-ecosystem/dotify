import re
from dotify_lib.namespace import Namespace, DotifyNamespace

_TEMPLATE_PLACEHOLDER = re.compile(r"{{\s*(.*?)\s*}}")


def resolve(string: str, namespace: Namespace) -> str:
    def replacer(match: re.Match):
        content = match.group(1).strip()
        fields = content.split(".")

        subspace = namespace
        for field in fields:
            sub_fields = subspace.get_fields()
            if field not in sub_fields:
                print(
                    f"[ERROR] Unable to find field `{field}` for namespace: {subspace}"
                )
                exit(-1)
            subspace = sub_fields[field]
        return str(subspace)

    return _TEMPLATE_PLACEHOLDER.sub(replacer, string)
