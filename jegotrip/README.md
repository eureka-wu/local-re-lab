# 无忧行 (JegoTrip) App 逆向与技术特征分析

## 1. 基础信息
- **Package Name**: `com.cmi.jegotrip`
- **Version**: `8.9.6.0`
- **File**: `jegotrip_v8.9.6.0.apk`
- **出品方**: 中国移动国际有限公司 (CMI, China Mobile International)

## 2. 技术架构
- **跨平台技术栈**: React Native (包含 `assets/index.android.bundle`，约 13.5MB 明文 JS 代码)
- **原生桥接**: `NativeModules.JegoTripRN` (`g.jegoWrapper`)
- **通信底层 (VoIP / SMS)**: 集成菊风 Juphoon (JusTalk Cloud) 通信 SDK，本地存储使用 Realm (`ConversationLog`, `MessageLog`)
- **推送体系**: 华为 Push、小米 Push、荣耀 Push、vivo Push、百度 Push
- **后台保活**: 针对主流 Android 厂商（小米、华为、OPPO、vivo、三星）定制了后台电量白名单与唤醒逻辑

## 3. 安全与风控
- **SSL Pinning**: `assets/app2.cer` (Subject: CMI Shenzhen Jegotrip) 与 `assets/srca.cer` 在 `com.cmi.jegotrip.application.SysApplication` 中直接绑定
  - *抓包注意*: 使用 mitmproxy 等抓包工具时，必须先在测试机通过 Frida 或 LSPosed (JustTrustMe) 绕过 SSL Pinning，否则会报握手失败。
- **设备风控**: 阿里聚安全反欺诈 SDK (`libaliyunaf.so`)
- **实名与活体**: 公安一所 eID (`libeidjni.so`)、百度人脸识别与身份证 OCR (`libfacedevice.so`, `libidcard_quality.so`)

## 4. 核心服务端域名
- 业务 API: `https://szsvapp.jegotrip.com.cn`、`https://szsvopenapi.jegotrip.com.cn`
- 静态 CDN: `https://jtoss.jegotrip.com.cn`、`https://cdn.jegotrip.com.cn`

