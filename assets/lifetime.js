/* Explicit user gestures only: no automatic redirects or checkout, and no URL-provided price. */
(() => {
  const app = document.body.dataset.app;
  const labels = {
    en: {
      language: 'Language', title: `Lifetime access,\ninside ${app}.`,
      intro: 'Check the current price and available offers in the app. You confirm your purchase securely in Google Play.',
      open: `Open ${app}`,
      hint: 'Open this page on your Android device. Opening the app will not make a purchase.',
      helpTitle: 'App didn’t open?', stepOne: `Install or update ${app} from Google Play.`,
      store: 'Install or update', stepTwo: `Open ${app} directly from your home screen.`,
      stepThree: 'Go to Settings, then choose Lifetime access in the purchase section.',
      restore: 'Already purchased? Choose Restore purchases in the app using the same Google Play account.',
      availability: 'The app and Google Play show purchase availability and the final price. This page does not reserve an offer.',
      privacy: 'Privacy', support: 'Contact support',
    },
    ko: {
      language: '언어', title: `평생 이용권은\n${app} 앱에서.`,
      intro: '앱에서 현재 가격과 적용 가능한 혜택을 확인하세요. 구매는 Google Play에서 직접 확인한 뒤 진행됩니다.',
      open: `${app} 열기`,
      hint: 'Android 기기에서 이 페이지를 열어 주세요. 앱을 여는 것만으로는 결제되지 않습니다.',
      helpTitle: '앱이 열리지 않나요?', stepOne: `Google Play에서 ${app} 앱을 설치하거나 업데이트하세요.`,
      store: '설치 또는 업데이트', stepTwo: `홈 화면에서 ${app} 앱을 직접 여세요.`,
      stepThree: '설정의 구매 항목에서 평생 이용권을 선택하세요.',
      restore: '이미 구매하셨나요? 구매에 사용한 Google Play 계정으로 앱에서 구매 복원을 선택하세요.',
      availability: '구매 가능 여부와 최종 가격은 앱과 Google Play에 표시됩니다. 이 페이지에서 할인 혜택이 예약되지는 않습니다.',
      privacy: '개인정보처리방침', support: '문의하기',
    },
  };
  const select = document.getElementById('language');
  function render(language) {
    const copy = labels[language] || labels.en;
    document.documentElement.lang = language in labels ? language : 'en';
    select.value = document.documentElement.lang;
    document.querySelectorAll('[data-copy]').forEach(element => {
      element.textContent = copy[element.dataset.copy];
    });
  }
  select.addEventListener('change', () => render(select.value));
  render(navigator.language.toLowerCase().startsWith('ko') ? 'ko' : 'en');
  // A desktop or iOS browser cannot open an Android package. Keep installation help visible.
  document.getElementById('open-app').hidden = !/Android/i.test(navigator.userAgent);
})();
