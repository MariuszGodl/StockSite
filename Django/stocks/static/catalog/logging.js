
// Auth modal logic
document.getElementById('loginBtn').addEventListener('click', ()=>openAuth('login'));
document.getElementById('signupBtn').addEventListener('click', ()=>openAuth('signup'));
document.getElementById('closeAuth').addEventListener('click', closeAuth);
document.getElementById('switchToSignup').addEventListener('click', ()=>openAuth('signup'));

function openAuth(mode){
document.getElementById('authModal').classList.add('active');
document.getElementById('authTitle').textContent = mode === 'login' ? 'Log In' : 'Sign Up';
document.getElementById('authSubmit').textContent = mode === 'login' ? 'Log In' : 'Create account';
}
function closeAuth(){ document.getElementById('authModal').classList.remove('active'); }