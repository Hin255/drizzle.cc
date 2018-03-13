rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default
ln -s -f /root/web_hannah/bbs.conf /etc/supervisor/conf.d/hannah_bbs.conf
ln -s -f /root/web_hannah/bbs.nginx /etc/nginx/sites-enabled/hannah_bbs
ln -s -f /root/web_hannah/mongodb.conf /etc/supervisor/conf.d/mongodb.conf
service supervisor restart
service nginx restart
echo 'deploy success'
