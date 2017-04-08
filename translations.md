Translations README
===================

1. Modify templates. Use {{ gettext('text') }} to show "text" localized in en/fi.

2. Run:

pybabel extract -F babel.cfg -o messages.pot .
pybabel update -i messages.pot -d translations

3. Add localizations to translations/fi/LC_MESSAGES/messages.po

4. Run pybabel compile -d translations