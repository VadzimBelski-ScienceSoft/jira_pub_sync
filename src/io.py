from datetime import datetime as dt, timedelta as td, timezone
import click
from src.config import Issue, JiraConfig
import re


class IO:
    STATUS_COLOR = {'info': 'white', 'error': 'red', 'warning': 'yellow', 'success': 'green'}

    @classmethod
    def input_days_ago(cls):
        num = 0
        while num < 1:
            num = click.prompt('Please enter a number of days', type=int)

        return dt.today() - td(days=num - 1)

    @classmethod
    def input_jira_credentials(cls, url=None, username=None, password=None):
        url = click.prompt('Host url', value_proc=cls.url_validation, default=url)
        username = click.prompt('Username', default=username, type=str)
        password = click.prompt('Password' if password is None else 'Password [hidden]', hide_input=True, type=str,
                                default=password, show_default=False)

        return JiraConfig(url, username, password)

    @classmethod
    def url_validation(cls, url):
        r = re.match("^https?:\/\/[\w\-\.]+\.[a-z]{2,6}\.?(\/[\w\.]*)*\/?$", url)
        if r is None:
            raise click.UsageError('Please, type valid URL')

        return url

    @classmethod
    def highlight_key(cls, url, color='cyan'):
        if url:
            key = Issue.parse_key(url)
            return url.replace(key, click.style(key, fg=color))

        return None

    @classmethod
    def print_date_line(cls, date, on_nl=True):
        if on_nl:
            click.echo()

        click.echo(date.strftime('%d %B %Y, %A'))

    @classmethod
    def print_time_diff_line(cls, pub_issue, sk_link, time_diff):
        hours = str(time_diff / 3600) + 'h'

        status = 'error'
        if time_diff == 0:
            status = 'info'
            hours = '0h'
        elif time_diff > 0:
            status = 'success'
            hours = '+' + hours

        cls.print_line(pub_issue, sk_link, hours, status=status)

    @classmethod
    def print_line(cls, pub_issue, sk_link, message, status='info', color=None):
        if not color:
            color = cls.STATUS_COLOR.get(status, 'white')

        pub_link = IO.highlight_key(pub_issue.permalink())
        sk_link = IO.highlight_key(sk_link)

        message = click.style(message, fg=color)
        summary = pub_issue.truncate_summary()

        click.echo('%s => %s [ %s ] %s' % (pub_link, sk_link, message, summary))
