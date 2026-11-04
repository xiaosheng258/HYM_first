// 仪表盘交互逻辑
 document.addEventListener('DOMContentLoaded', function() {
    // 获取导航项和卡片元素
    const navItems = document.querySelectorAll('.nav-item');
    const cards = document.querySelectorAll('.card');
    const logoutBtn = document.getElementById('logout-btn');
    
    // 初始化导航事件监听
    initNavigation();
    
    // 初始化退出登录功能
    initLogout();
    
    // 初始化其他交互功能
    initInteractions();
    
    // 导航切换功能
    function initNavigation() {
        navItems.forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                
                // 获取目标卡片ID
                const targetId = this.getAttribute('data-target');
                
                // 移除所有导航项的活动状态
                navItems.forEach(nav => nav.classList.remove('active'));
                
                // 添加当前导航项的活动状态
                this.classList.add('active');
                
                // 隐藏所有卡片
                cards.forEach(card => card.classList.remove('active'));
                
                // 显示目标卡片
                const targetCard = document.getElementById(targetId);
                if (targetCard) {
                    targetCard.classList.add('active');
                    
                    // 添加页面切换动画
                    targetCard.style.opacity = '0';
                    setTimeout(() => {
                        targetCard.style.opacity = '1';
                    }, 50);
                }
            });
        });
    }
    
    // 退出登录功能
    function initLogout() {
        logoutBtn.addEventListener('click', function() {
            if (confirm('确定要退出登录吗？')) {
                // 跳转到登录页面
                window.location.href = 'index.html';
            }
        });
    }
    
    // 其他交互功能初始化
    function initInteractions() {
        // 用户管理页面交互
        initUserManagement();
        
        // ICT学院课程卡片交互
        initCourseCards();
        
        // 添加卡片悬停效果
        addCardHoverEffects();
    }
    
    // 用户管理交互
    function initUserManagement() {
        const editProfileBtn = document.querySelector('.edit-profile-btn');
        const addUserBtn = document.querySelector('.add-user-btn');
        const actionBtns = document.querySelectorAll('.action-btn');
        
        // 编辑个人资料
        if (editProfileBtn) {
            editProfileBtn.addEventListener('click', function() {
                alert('编辑个人资料功能开发中...');
            });
        }
        
        // 添加用户
        if (addUserBtn) {
            addUserBtn.addEventListener('click', function() {
                alert('添加用户功能开发中...');
            });
        }
        
        // 用户操作按钮
        actionBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const action = this.classList.contains('edit') ? '编辑' : '删除';
                const username = this.closest('tr').querySelector('td:nth-child(2)').textContent;
                
                if (action === '删除') {
                    if (confirm(`确定要删除用户 "${username}" 吗？`)) {
                        alert(`用户 "${username}" 删除成功！`);
                        // 实际项目中这里应该调用API删除用户并刷新表格
                    }
                } else {
                    alert(`编辑用户 "${username}" 功能开发中...`);
                }
            });
        });
    }
    
    // 课程卡片交互
    function initCourseCards() {
        const courseCards = document.querySelectorAll('.course-card');
        const viewAllBtn = document.querySelector('.view-all-courses-btn');
        
        // 课程卡片点击
        courseCards.forEach(card => {
            card.addEventListener('click', function() {
                const courseName = this.querySelector('h4').textContent;
                alert(`课程 "${courseName}" 详情页面开发中...`);
            });
        });
        
        // 查看全部课程
        if (viewAllBtn) {
            viewAllBtn.addEventListener('click', function() {
                alert('课程列表页面开发中...');
            });
        }
    }
    
    // 卡片悬停效果
    function addCardHoverEffects() {
        const featureCards = document.querySelectorAll('.feature-card, .harmony-feature-card');
        
        featureCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-4px)';
                this.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.12)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.06)';
            });
        });
    }
    
    // 添加平滑滚动效果
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            if (this.getAttribute('href') === '#') return;
            
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // 模拟数据加载效果
    simulateDataLoading();
    
    function simulateDataLoading() {
        // 为各个卡片添加淡入效果
        setTimeout(() => {
            const activeCard = document.querySelector('.card.active');
            if (activeCard) {
                activeCard.style.opacity = '1';
            }
        }, 100);
    }
    
    // 响应式导航处理
    handleResponsiveNavigation();
    
    function handleResponsiveNavigation() {
        function checkScreenSize() {
            const isMobile = window.innerWidth <= 768;
            const headerRight = document.querySelector('.header-right');
            const headerLeft = document.querySelector('.header-left');
            
            if (isMobile) {
                // 移动端布局调整
                headerRight.style.position = 'relative';
                headerRight.style.right = 'auto';
                headerRight.style.top = 'auto';
                headerRight.style.transform = 'none';
                headerRight.style.marginTop = '16px';
                headerRight.style.textAlign = 'center';
                
                // 将header-right移到header-left下方
                if (headerRight.parentElement === document.querySelector('.dashboard-header')) {
                    document.querySelector('.dashboard-header').insertBefore(
                        document.createElement('div'),
                        headerRight
                    ).appendChild(headerRight);
                }
            } else {
                // 桌面端布局恢复
                headerRight.style.position = 'absolute';
                headerRight.style.right = '20px';
                headerRight.style.top = '50%';
                headerRight.style.transform = 'translateY(-50%)';
                headerRight.style.marginTop = '0';
                headerRight.style.textAlign = 'left';
            }
        }
        
        // 初始检查
        checkScreenSize();
        
        // 监听窗口大小变化
        window.addEventListener('resize', checkScreenSize);
    }
    
    // 为用户页面表格添加排序功能（简单演示）
    addTableSorting();
    
    function addTableSorting() {
        const userTable = document.querySelector('.user-table');
        if (userTable) {
            const headers = userTable.querySelectorAll('th');
            
            headers.forEach(header => {
                header.addEventListener('click', function() {
                    const columnIndex = Array.from(headers).indexOf(this);
                    const rows = Array.from(userTable.querySelectorAll('tbody tr'));
                    
                    // 简单排序演示
                    rows.sort((a, b) => {
                        const aValue = a.cells[columnIndex].textContent.trim();
                        const bValue = b.cells[columnIndex].textContent.trim();
                        
                        return aValue.localeCompare(bValue);
                    });
                    
                    // 重新排列行
                    const tbody = userTable.querySelector('tbody');
                    rows.forEach(row => tbody.appendChild(row));
                    
                    // 添加排序指示器
                    headers.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
                    this.classList.add('sorted-asc');
                });
            });
        }
    }
    
    // 添加键盘导航支持
    addKeyboardNavigation();
    
    function addKeyboardNavigation() {
        document.addEventListener('keydown', function(e) {
            // 使用方向键切换导航项
            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                const activeNav = document.querySelector('.nav-item.active');
                const navItemsArray = Array.from(navItems);
                const currentIndex = navItemsArray.indexOf(activeNav);
                
                let newIndex;
                if (e.key === 'ArrowLeft') {
                    newIndex = (currentIndex - 1 + navItemsArray.length) % navItemsArray.length;
                } else {
                    newIndex = (currentIndex + 1) % navItemsArray.length;
                }
                
                navItemsArray[newIndex].click();
            }
            
            // ESC键退出登录
            if (e.key === 'Escape') {
                logoutBtn.focus();
            }
        });
    }
});