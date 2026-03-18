// 登录表单处理
 document.addEventListener('DOMContentLoaded', function() {
    // 直接获取表单元素，确保正确绑定
    const form = document.querySelector('.login-form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    console.log('登录表单已加载');
    
    // 表单提交处理 - 直接绑定到form元素
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // 阻止表单默认提交
            console.log('表单提交事件触发');
            
            // 获取用户输入
            const username = usernameInput.value.trim();
            const password = passwordInput.value.trim();
            
            console.log('用户输入:', { username, password: '******' });
            
            // 简单的表单验证
            if (!validateForm(username, password)) {
                return;
            }
            
            // 模拟登录请求（实际项目中应替换为真实的API调用）
            simulateLogin(username, password);
        });
    } else {
        console.error('未找到登录表单元素');
    }
    
    // 表单验证函数
    function validateForm(username, password) {
        let isValid = true;
        
        // 清除之前的错误提示
        clearErrors();
        
        // 用户名验证
        if (username === '') {
            showError(usernameInput, '请输入用户名');
            isValid = false;
        }
        
        // 密码验证
        if (password === '') {
            showError(passwordInput, '请输入密码');
            isValid = false;
        } else if (password.length < 6) {
            showError(passwordInput, '密码长度不能少于6位');
            isValid = false;
        }
        
        return isValid;
    }
    
    // 显示错误提示
    function showError(inputElement, errorMessage) {
        const formGroup = inputElement.parentElement;
        
        // 创建错误提示元素
        const errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.textContent = errorMessage;
        
        // 添加错误样式到输入框
        inputElement.classList.add('error');
        
        // 将错误提示添加到表单组
        formGroup.appendChild(errorElement);
        
        // 输入框聚焦时清除错误
        inputElement.addEventListener('focus', function() {
            clearInputError(inputElement);
        }, { once: true });
    }
    
    // 清除特定输入框的错误
    function clearInputError(inputElement) {
        const formGroup = inputElement.parentElement;
        const errorElement = formGroup.querySelector('.error-message');
        
        if (errorElement) {
            formGroup.removeChild(errorElement);
        }
        
        inputElement.classList.remove('error');
    }
    
    // 清除所有错误提示
    function clearErrors() {
        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(message => message.remove());
        
        const errorInputs = document.querySelectorAll('input.error');
        errorInputs.forEach(input => input.classList.remove('error'));
    }
    
    // 模拟登录请求
    function simulateLogin(username, password) {
        // 显示加载状态
        const loginButton = document.querySelector('.login-button');
        const originalButtonText = loginButton.textContent;
        loginButton.disabled = true;
        loginButton.textContent = '登录中...';
        
        // 模拟网络延迟
        setTimeout(function() {
            // 简单的模拟验证（实际项目中应替换为真实的后端验证）
            // 这里使用用户名和密码都为"admin"作为演示
            console.log('进行登录验证');
            if (username === 'admin' && password === 'admin') {
                console.log('登录验证成功');
                
                // 登录成功
                showNotification('登录成功！正在跳转...', 'success');
                
                // 直接跳转，减少延迟，确保能立即看到效果
                console.log('即将跳转到dashboard.html');
                window.location.href = 'dashboard.html';
                
                // 备用方案 - 如果上面的跳转失败，使用这个
                setTimeout(function() {
                    console.log('备用跳转触发');
                    window.location.replace('dashboard.html');
                }, 500);
            } else {
                // 登录失败
                showNotification('用户名或密码错误，请重试', 'error');
                loginButton.disabled = false;
                loginButton.textContent = originalButtonText;
            }
        }, 1500);
    }
    
    // 显示通知消息
    function showNotification(message, type) {
        // 创建通知元素
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // 添加到页面
        document.body.appendChild(notification);
        
        // 显示动画
        setTimeout(function() {
            notification.classList.add('show');
        }, 10);
        
        // 自动消失
        setTimeout(function() {
            notification.classList.remove('show');
            setTimeout(function() {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    // 添加错误样式（动态CSS）
    const style = document.createElement('style');
    style.textContent = `
        .error-message {
            color: #e53e3e;
            font-size: 12px;
            margin-top: 5px;
        }
        
        input.error {
            border-color: #e53e3e;
        }
        
        input.error:focus {
            box-shadow: 0 0 0 3px rgba(229, 62, 62, 0.1);
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: -400px;
            padding: 12px 20px;
            border-radius: 4px;
            color: white;
            font-size: 14px;
            z-index: 9999;
            transition: right 0.3s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .notification.show {
            right: 20px;
        }
        
        .notification-success {
            background-color: #38a169;
        }
        
        .notification-error {
            background-color: #e53e3e;
        }
    `;
    document.head.appendChild(style);
    
    // 记住用户名功能（可选）
    // 在实际项目中，可以使用localStorage或cookie来实现
    
    // 添加键盘事件处理
    passwordInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            loginForm.dispatchEvent(new Event('submit'));
        }
    });
});