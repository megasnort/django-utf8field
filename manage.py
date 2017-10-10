#!/usr/bin/env python
import os                        # pragma: no cover
import sys                       # pragma: no cover

if __name__ == "__main__":       # pragma: no cover
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "utf8field.tests.settings")

    from django.core.management import execute_from_command_line

    is_testing = 'test' in sys.argv

    if is_testing:
        import coverage

        cover_only_these_apps = [x.split('.')[0] for x in sys.argv[2:] if x[0] != '-' and not x.isdigit()]

        if not cover_only_these_apps:
            cover_only_these_apps = ['.']

        cov = coverage.coverage(source=cover_only_these_apps, omit=['*/tests/*'])
        cov.erase()
        cov.start()

    execute_from_command_line(sys.argv)

    if is_testing:
        cov.stop()
        cov.save()
        cov.report()
