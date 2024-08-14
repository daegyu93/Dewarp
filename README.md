## Prepare 
```bash
./install_requriement.sh
```

## Dewarp 
1. config 파일 직접 입력 
```bash
./dewarp_config.sh [camera_number] [config_file_path]
```

2. config 파일 eeprom 에서 읽어서 적용 ( config/dewarper_config_[camera_nubmer] 로 config 파일 저장됨 )
```bash
./dewarp_eeprom.sh [camera_number]
```

## Dewarp 되기 전 이미지 
```bash
./normal.sh [camera_number]
```