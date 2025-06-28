// RiseWith 웹앱 자동 스크린샷 도구
// 사용법: node screenshot_tool.js

const puppeteer = require('puppeteer');
const path = require('path');

async function takeScreenshot() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // 화면 크기 설정
  await page.setViewport({ width: 1920, height: 1080 });
  
  try {
    // RiseWith 앱 페이지로 이동
    await page.goto('http://localhost:3000', { waitUntil: 'networkidle2' });
    
    // 페이지가 완전히 로드될 때까지 대기
    await page.waitForTimeout(2000);
    
    // 스크린샷 저장
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `RiseWith_Auto_Screenshot_${timestamp}.png`;
    
    await page.screenshot({ 
      path: filename, 
      fullPage: true,
      quality: 100 
    });
    
    console.log(`✅ 스크린샷 저장 완료: ${filename}`);
    
    // 로그인 페이지 스크린샷도 생성
    await page.goto('http://localhost:3000/login', { waitUntil: 'networkidle2' });
    await page.waitForTimeout(1000);
    
    const loginFilename = `RiseWith_Login_Screenshot_${timestamp}.png`;
    await page.screenshot({ 
      path: loginFilename, 
      fullPage: true,
      quality: 100 
    });
    
    console.log(`✅ 로그인 페이지 스크린샷 저장 완료: ${loginFilename}`);
    
  } catch (error) {
    console.error('❌ 스크린샷 생성 실패:', error);
  } finally {
    await browser.close();
  }
}

// 실행
takeScreenshot().catch(console.error);
