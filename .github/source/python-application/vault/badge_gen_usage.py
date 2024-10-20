# NOTE: This is getting the last file edited with the
# NOTE: extension (.svg) and with the starting point. (gen.)
# NOTE: And then it checks if it is not the same one as the current version

related_entries = [entry for entry in glob.glob(r'.\storage\gen.*.svg') if not entry.endswith(f'{parsed["version"]}.svg')]
possibly_latest_entry = related_entries[-1] if related_entries.__len__() > 0 else None

if possibly_latest_entry:
    content = open(possibly_latest_entry, 'r').read()

    # NOTE: If it is a valid generated file
    # NOTE: and if it hasn't been replaced the Badge already.
    if content.startswith('<svg ') and "{REPLACEMENT_START}" in content:
        # Scalable Vector original badge
        original = content.split('{REPLACEMENT_START}')[1].split('{REPLACEMENT_STOP}')[0].rsplit("\n", 1)[0]
        # Current Scalable Vector badge
        alpha = content.split('{ORG_REPLACEMENT_START} -->')[1].split('<!--')[0].rsplit("\n", 1)[0]

        content = content.replace(alpha, original)

        # Replace scalable data
        content = content.replace(
            '<!-- Replacement (for branch icon ect..)' + 
            content.split('<!-- Replacement (for branch icon ect..)')[1].split('-->')[0] + '-->', '').replace(
        '</div>\n                        \n                    </h2>',
        '</div>\n                    </h2>').replace('<!-- {ORG_REPLACEMENT_START} -->\n', '<!-- Completed badge replacement -->').replace('//', '/')

        with open(possibly_latest_entry, 'w') as entry:
            entry.write(content)