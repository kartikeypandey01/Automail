echo mail.sh called: `date` > /mnt/c/Users/user/onedrive/desktop/email_script/cronlog.txt
cd /mnt/c/Users/user/onedrive/desktop/email_script
/usr/bin/python3 /mnt/c/Users/user/onedrive/desktop/email_script/mail_script.py > /mnt/c/Users/user/onedrive/desktop/email_script/cron_log.log 2>&1
