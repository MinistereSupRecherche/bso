"""Connect to ftp."""
from ftplib import FTP
from ..config import BaseConfig


def ftp_connect(dest="preprod"):
    """Connexion to ftp server."""
    conn = FTP(
        BaseConfig.FTP_HOST,
        BaseConfig.FTP_USER,
        BaseConfig.FTP_PASSWORD
    )
    assert dest in ('preprod', 'prod'), f"Bad destination '{dest}'"
    if dest == 'preprod':
        conn.cwd(BaseConfig.FTP_SCANR_PREPROD_DIR)
        return conn
    if dest == 'prod':
        conn.cwd(BaseConfig.FTP_SCANR_PROD_DIR)
        return conn
