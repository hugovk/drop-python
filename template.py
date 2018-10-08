import argparse
import datetime
import os
from string import Template

from utils import create_dir

SUBSTITUTIONS = {
    "2.0": {"template_eol": "2001-06-22"},
    "2.1": {"template_eol": "2002-04-08"},
    "2.2": {"template_eol": "2003-05-30"},
    "2.3": {"template_eol": "2008-03-11"},
    "2.4": {"template_eol": "19 December 2008"},
    "2.5": {"template_eol": "26 May 2011"},
    "2.6": {
        "template_eol": "29 October 2013",
        "reasons": """
                    <li><a href="https://pip.pypa.io/en/stable/news/">pip no longer supports Python {{version}}</a></li>
                    <li><a href="https://snarky.ca/stop-using-python-2-6/">Stop using Python 2.6 please</a></li>
                    <li><a href="https://www.curiousefficiency.org/posts/2015/04/stop-supporting-python26.html">Stop Supporting Python 2.6 (For Free)</a></li>
                    <li><a href="https://www.python3statement.org/">Scientific Python moving to require Python 3</a></li>
                    <li><a href="https://github.com/pypa/pip/issues/3796">Not much PyPI traffic (June 2016)</a></li>
                    <li><a href="https://medium.com/@hugovk/python-version-share-over-time-cf4498822650">Virtually no PyPI traffic (June 2018)</a></li>
""",
        "remove": """
                    <p>For example, no need to install or import unittest2 any more. This:</p>
                        <pre>
try:
    import unittest2 as unittest  # Python 2.6
 except ImportError:
    import unittest</pre>
                    <p>&hellip;can be replaced with:
                        <pre>
import unittest</pre>
""",
        "new_features": """
                    <h3 id="new-features">Use new Python features</h3>
                    <p>See <a href="https://docs.python.org/3/whatsnew/2.7.html">what's new</a>. For example:

                        <ul>
                            <li><p>Use <a href="https://renzo.lucioni.xyz/pythons-set-literals/">set literals</a>:</p>
                                <pre>
set([1, 2, 3])  # This can be replaced...
{1, 2, 3}       # ... with this</pre>

                            <li><p>Update <a href="https://pyformat.info/">string formatters</a>:</p>
                                <pre>
# These can be replaced...
'%s %s' % ('one', 'two')
'{1} {2}'.format('one', 'two')

# ... with this
'{} {}'.format('one', 'two')</pre>

                            <li>Use <code>OrderedDict</code> and <code>Counter</code> from <code>collections</code>
                        </ul>

""",
    },
    "2.7": {
        "template_eol": "1 January 2020",
        "reasons": """
                    <li><a href="https://pythonclock.org/">Python 2.7 Countdown</a></li>
                    <li><a href="https://python3statement.org/">Sunsetting Python 2 support</a></li>
                    <li><a href="https://whypy3.com/">Why Python 3?</a></li>
""",
        "remove": """
                    <p>Follow this guide: <a href="https://python3statement.org/practicalities/">https://python3statement.org/practicalities/</a>
""",
    },
    "3.0": {"template_eol": "27 June 2009"},
    "3.1": {"template_eol": "9 April 2012"},
    "3.2": {"template_eol": "27 February 2016"},
    "3.3": {
        "template_eol": "29 September 2017",
        "reasons": """
                    <li><a href="https://github.com/pypa/pip/issues/3796">pip 10 deprecated Python 3.3 support, pip 11 won't support it</a></li>
                    <li><a href="https://github.com/pypa/pip/issues/3796">Very little PyPI traffic (June 2016)</a></li>
                    <li><a href="https://medium.com/@hugovk/python-version-share-over-time-cf4498822650">Virtually no PyPI traffic (June 2018)</a></li>
""",
    },
    "3.4": {"template_eol": "16 March 2019", "reasons": "<li>It's EOL</li>"},
}

REASONS = """
                    <li><a href="https://pip.pypa.io/en/stable/news/">pip no longer supports Python {{version}}</a></li>
                    <li><a href="https://bitbucket.org/ned/coveragepy/">Coverage no longer supports Python {{version}}</a></li>
                    <li><a href="https://www.python3statement.org/">Requests no longer supports Python {{version}}</a></li>
                    <li><a href="https://github.com/pypa/pip/issues/3796">Virtually no PyPI traffic (June 2016)</a></li>
                    <li><a href="https://medium.com/@hugovk/python-version-share-over-time-cf4498822650">Virtually no PyPI traffic (June 2018)</a></li>

"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Template", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-v",
        "--version",
        default=["2.6", "3.2", "3.3"],
        nargs="+",
        help="Python version or versions to check",
    )
    args = parser.parse_args()

    # Open the file
    with open("template/index.html") as infile:
        # Read it
        src = Template(infile.read())

        now = datetime.datetime.utcnow()
        for version in args.version:

            # Document data
            print(version)
            major, minor = version.split(".")
            next_minor = int(minor) + 1
            next_version = f"{major}.{next_minor}"
            substitutions = SUBSTITUTIONS[version]
            d = {
                "template_version": version,
                "template_eol": substitutions["template_eol"],
                "template_major": major,
                "template_minor": minor,
                "template_next_minor": next_minor,
                "template_next_version": next_version,
                "template_reasons": substitutions.get("reasons", REASONS),
                "template_remove_examples": substitutions.get("remove", ""),
                "template_new_features": substitutions.get("new_features", ""),
            }

            # Do the substitution
            result = src.safe_substitute(d)

            try:
                # 1 January 2020
                eol = datetime.datetime.strptime(
                    substitutions["template_eol"], "%d %B %Y"
                )
            except ValueError:
                # 2020-01-01
                eol = datetime.datetime.strptime(
                    substitutions["template_eol"], "%Y-%m-%d"
                )

            # EOL in the future?
            if now < eol:
                result = result.replace("about time", "soon time")
                result = result.replace(" reached the ", " reaches the ")
            # print(result)

            # Save it
            outfile = os.path.join(version, "index.html")
            print(outfile)
            create_dir(version)
            with open(outfile, "w") as f:
                f.write(result)
