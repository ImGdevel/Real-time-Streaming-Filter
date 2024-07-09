

#  OBLIND | Real-time-Streaming-Filter
<img src="https://github.com/ImGdevel/Real-time-Streaming-Filter/assets/62339794/408bf0f5-52bc-4a90-9716-28a0acacacf7" alt="image" width="680" height="400">

실시간 스트리밍 데이터를 효율적으로 처리하고 필터링하는 강력한 애플리케이션입니다.


## 빠른 시작
빌드버전 다운로드<br>
https://drive.google.com/file/d/1j6hMPa1un8TR8fsX2P9NtMW6TSgmluGy/view?usp=drive_link

## 목차

- [소개](#소개)
- [특징](#특징)
- [설치](#설치)
- [사용법](#사용법)
- [구성](#구성)
- [기여](#기여)
- [라이선스](#라이선스)

## 소개

`Real-time-Streaming-Filter`는 다양한 스트리밍 데이터 소스에 대해 강력한 실시간 필터링 기능을 제공하는 애플리케이션입니다. 여러 필터 기준을 지원하며, 최소한의 지연 시간으로 고처리량 데이터 스트림을 처리할 수 있습니다.

## 특징

## 특징

- **실시간 처리:** 웹캠과 같이 실시간으로 전송되는 영상을 필터링할 수 있습니다.
- **객체 및 얼굴 인식:** YOLO와 DLIB을 사용하여 사람의 얼굴과 객체를 인식하고 모자이크 처리를 적용할 수 있습니다.
- **사용자 정의 필터:** 사용자가 원하지 않는 객체나 인물을 모자이크 등으로 필터링할 수 있으며, 필터링 항목을 설정하고 관리할 수 있습니다.
- **다양한 입력 및 출력:** 웹캠, 동영상 파일, 이미지 파일 등 다양한 입력 소스를 지원하며, 필터링된 영상을 화면에 출력하거나 파일로 저장할 수 있습니다.
- **UI를 통한 간편한 설정:** 웹캠 실시간 필터링, 동영상 파일 필터링, 사진 필터링 기능을 UI를 통해 선택할 수 있으며, 세부 설정을 관리할 수 있습니다.
- **예외 처리 및 경고:** 기능별 예외 발생 시 경고문을 출력하여 사용자에게 알립니다.
- **필터링 이미지 등록:** 사용자가 원하는 필터링 이미지를 등록하고 선택할 수 있으며, 블러의 강도, 크기, 형태를 조절할 수 있습니다.
- **효율성:** 객체 추적 및 작은 객체 탐지를 위한 이미지 사이즈 조정과 타일링을 통해 더 정확한 인물 탐지 및 필터링을 수행합니다.
- **화면 녹화:** 실시간 영상에서 화면 녹화를 할 수 있으며, 사용자가 지정한 영역을 녹화할 수 있습니다.
- **실용성:** 방송인의 사생활 보호와 법적 문제를 피할 수 있도록 실시간 야외 방송 콘텐츠에서 유용하게 사용할 수 있습니다.
- **경제성:** 검열 작업의 자동화를 통해 시간과 자원을 절약할 수 있으며, 효율적인 방송 진행이 가능합니다.
- **미리보기 기능:** 사용자가 필터링된 이미지나 영상을 미리 확인할 수 있습니다.
- **간편한 설치:** 별도의 환경 설정 없이 실행할 수 있도록 Installer를 제공합니다.


## 설치

### 프로그램 실행 요구 사항



- [Python 3.10.6 이상](https://www.python.org/)

### 빌드 요구 사항

- [Python 3.10.6 이상](https://www.python.org/)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)
- [cuDNN](https://developer.nvidia.com/cudnn)
- [CMake](https://cmake.org/)

### 설치 단계

1. 저장소를 클론합니다:
    ```bash
    git clone https://github.com/your-username/real-time-streaming-filter.git
    cd real-time-streaming-filter
    ```

2. 가상 환경을 만들고 활성화합니다: (선택)
    ```bash
    python -m venv venv
    source venv/bin/activate  # 윈도우에서는 `venv\Scripts\activate` 사용
    ```

3. CUDA 버전에 맞는 PyTouch를 설치합니다. <br> 
    https://pytorch.org/get-started/locally/
    ```bash
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    혹은
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    ```

4. 필요한 패키지를 설치합니다:
    ```bash
    pip install -r requirements.txt
    ```

5. 빌드를 위한 추가 요구 사항을 확인하고 설치합니다:
    - [CUDA Toolkit 설치 가이드](https://developer.nvidia.com/cuda-toolkit)
    - [cuDNN 설치 가이드](https://developer.nvidia.com/cudnn)
    - [CMake 설치 가이드](https://cmake.org/install/)


## 사용법

### 기본 사용법

1. 애플리케이션을 시작합니다:
    ```bash
    python main.py
    ```

2. 자세한 프로그램 사용 방법은 Wiki를 참조하세요. <br>
https://github.com/ImGdevel/Real-time-Streaming-Filter/wiki
