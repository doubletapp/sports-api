## Local development

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```
CREATE DATABASE sports;
CREATE USER sports_admin WITH PASSWORD 'sports_admin';
GRANT ALL PRIVILEGES ON DATABASE sports TO sports_admin;
```

## Docker

```
sudo docker-compose up -d --build --force-recreate && \
sudo docker exec -it sports-api_app_1 python manage.py migrate && \
sudo docker exec -it sports-api_app_1 python manage.py collectstatic --no-input --clear
```


## Nginx
```
server {
    listen 80;
    server_name sports.doubletapp.ru;

    location / {
        proxy_pass http://localhost:1337;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

## ffmpeg

### cut video
example bash:
```
ffmpeg -ss 10.123 -i input1.mp4 -to 10.454 -c copy output.mp4 -y
```

example code:
```
f'ffmpeg -ss {start_fragment_shift} -i input1.mp4 -to {fragment_duration} -c copy {fragment_name}.mp4 -y'
```

### concat videos ffmpeg
example bash:
```
ffmpeg -i input1.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts input1.ts -y
ffmpeg -i input2.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts input2.ts -y
ffmpeg -i "concat:input1.ts|input2.ts" -c copy -bsf:a aac_adtstoasc output.mp4 -y
```

example code:
```
f'ffmpeg -i {fragment_1_name}.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts {fragment_1_name}.ts -y'
f'ffmpeg -i {fragment_2_name}.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts {fragment_2_name}.ts -y'
f'ffmpeg -i {fragment_n_name}.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts {fragment_n_name}.ts -y'
f'ffmpeg -i "concat:{fragment_1_name}.ts|{fragment_2_name}.ts|{fragment_n_name}.ts" -c copy -bsf:a aac_adtstoasc {highlight_name}.mp4 -y'
```
