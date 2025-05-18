// 진정난수 시드 생성 (128bit hex)
function generateRandomSeed() {
  const arr = new Uint8Array(16);
  window.crypto.getRandomValues(arr);
  return Array.from(arr)
    .map(b => b.toString(16).padStart(2,'0'))
    .join('');
}

// 시드 생성 & 복사
document.querySelectorAll('#generate-seed').forEach(btn =>
  btn.addEventListener('click', () => {
    const input = btn.parentElement.querySelector('input[name="seed"]');
    input.value = generateRandomSeed();
    localStorage.seed = input.value;
  })
);
document.querySelectorAll('#copy-seed').forEach(btn =>
  btn.addEventListener('click', () => {
    const input = btn.parentElement.querySelector('input[name="seed"]');
    navigator.clipboard.writeText(input.value)
      .then(()=> alert('시드가 복사되었습니다!'));
  })
);

// 키스트림 복사
function copyKeystream() {
  const ks = document.getElementById('keystream');
  navigator.clipboard.writeText(ks.value)
    .then(()=> alert('키스트림이 복사되었습니다!'));
}

// 결과 복사 & 인덱스 저장
function copyOutput(id, msg) {
  const ta = document.getElementById(id);
  navigator.clipboard.writeText(ta.value).then(()=>{
    alert(msg);
    // 복사할 때 현재 체인 인덱스도 저장
    const idxIn = document.getElementById('chain_index');
    localStorage.chain_index = idxIn.value;
  });
}
