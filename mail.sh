echo mail.sh called: `date` > /mnt/c/Users/user/onedrive/desktop/email_script/cronlog.txt
#HOME = /mnt/c/Users/user/onedrive/desktop/email_script
#PYTHONPATH = /home/kp/.local/lib/python310/site-packages
cd /mnt/c/Users/user/onedrive/desktop/email_script
/usr/bin/python3 /mnt/c/Users/user/onedrive/desktop/email_script/mail_script.py > /mnt/c/Users/user/onedrive/desktop/email_script/cron_log.log 2>&1
