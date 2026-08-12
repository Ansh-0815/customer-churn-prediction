// Global Chart Instances
let doughnutChart, contractChart, internetChart, tenureChart, modelComparisonChart, monthlyChargesDistChart, servicesSecurityChart;

// Initialize Saved Theme on page load
const savedTheme = localStorage.getItem('theme_v2');
if (savedTheme === 'light') {
    document.body.classList.add('light-theme');
} else {
    document.body.classList.remove('light-theme');
}

// Toggle Theme Function
function toggleTheme() {
    const isLight = document.body.classList.toggle('light-theme');
    localStorage.setItem('theme_v2', isLight ? 'light' : 'dark');
    
    // Update chart colors dynamically
    const gridColor = isLight ? '#e2e8f0' : 'rgba(255, 255, 255, 0.05)';
    const textColor = isLight ? '#64748b' : '#94a3b8';
    
    const charts = [doughnutChart, contractChart, internetChart, tenureChart, modelComparisonChart, monthlyChargesDistChart, servicesSecurityChart];
    charts.forEach(chart => {
        if (!chart) return;
        
        // Update legend
        if (chart.options.plugins && chart.options.plugins.legend) {
            chart.options.plugins.legend.labels.color = textColor;
        }
        
        // Update scales (if they exist)
        if (chart.options.scales) {
            if (chart.options.scales.x) {
                chart.options.scales.x.ticks.color = textColor;
                if (chart.options.scales.x.grid) {
                    chart.options.scales.x.grid.color = gridColor;
                }
            }
            if (chart.options.scales.y) {
                chart.options.scales.y.ticks.color = textColor;
                if (chart.options.scales.y.grid) {
                    chart.options.scales.y.grid.color = gridColor;
                }
            }
        }
        chart.update();
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // Initialize progress bar widths from data attributes
    document.querySelectorAll('.progress-fill').forEach(fill => {
        const width = fill.getAttribute('data-width');
        if (width) {
            fill.style.width = width;
        }
    });

    // 1. Tab Navigation Routing
    const navItems = document.querySelectorAll('.nav-item');
    const tabContents = document.querySelectorAll('.tab-content');
    const pageTitle = document.getElementById('page-title');
    const pageSubtitle = document.getElementById('page-subtitle');

    const tabMetaData = {
        'overview-tab': {
            title: 'Executive Churn Dashboard',
            subtitle: 'Real-time customer risk intelligence and MLflow model telemetry.'
        },
        'predict-tab': {
            title: 'Customer Churn Predictor',
            subtitle: 'Input customer attributes to calculate instant risk probability.'
        },
        'training-tab': {
            title: 'MLflow Training Center',
            subtitle: 'Retrain models on new snapshots and track performance parameters.'
        },
        'eda-tab': {
            title: 'Exploratory Data Analysis',
            subtitle: 'Key data distributions, correlations, and feature exploration studies.'
        }
    };

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const tabId = item.getAttribute('data-tab');
            
            navItems.forEach(n => n.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active-content'));
            
            item.classList.add('active');
            const targetContent = document.getElementById(tabId);
            if (targetContent) {
                targetContent.classList.add('active-content');
            }

            // Update Header titles dynamically
            if (tabMetaData[tabId]) {
                pageTitle.textContent = tabMetaData[tabId].title;
                pageSubtitle.textContent = tabMetaData[tabId].subtitle;
            }
        });
    });

    // Chart options defaults for professional Greyish-White theme
    const chartDefaults = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: '#475569', font: { family: 'Outfit', size: 12, weight: '600' } }
            }
        },
        scales: {
            x: {
                ticks: { color: '#475569', font: { family: 'Outfit' } },
                grid: { color: '#e2e8f0' }
            },
            y: {
                ticks: { color: '#475569', font: { family: 'Outfit' } },
                grid: { color: '#e2e8f0' }
            }
        }
    };

    // 2a. Overall Churn Distribution Doughnut Chart
    const doughnutCtx = document.getElementById('doughnutChart').getContext('2d');
    doughnutChart = new Chart(doughnutCtx, {
        type: 'doughnut',
        data: {
            labels: ['Retained (No Churn)', 'Churned'],
            datasets: [{
                data: [5174, 1869],
                backgroundColor: ['#10b981', '#ef4444'],
                borderWidth: 3,
                borderColor: '#0f172a',
                hoverOffset: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', size: 12, weight: '600' } }
                }
            }
        }
    });

    // 2b. Churn Distribution by Contract Bar Chart
    const contractCtx = document.getElementById('contractChart').getContext('2d');
    contractChart = new Chart(contractCtx, {
        type: 'bar',
        data: {
            labels: ['Month-to-month', 'One year', 'Two year'],
            datasets: [
                {
                    label: 'Retained',
                    data: [2220, 1307, 1647],
                    backgroundColor: '#10b981',
                    borderRadius: 6
                },
                {
                    label: 'Churned',
                    data: [1655, 166, 48],
                    backgroundColor: '#ef4444',
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', size: 12, weight: '600' } }
                }
            },
            scales: {
                x: {
                    ticks: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans' } },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' }
                },
                y: {
                    ticks: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans' } },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' }
                }
            }
        }
    });

    // 2c. Churn by Internet Service Type Bar Chart
    const internetCtx = document.getElementById('internetChart').getContext('2d');
    internetChart = new Chart(internetCtx, {
        type: 'bar',
        data: {
            labels: ['DSL', 'Fiber Optic', 'No Internet'],
            datasets: [
                {
                    label: 'Retained',
                    data: [1962, 1799, 1413],
                    backgroundColor: '#6366f1',
                    borderRadius: 6
                },
                {
                    label: 'Churned',
                    data: [459, 1297, 113],
                    backgroundColor: '#06b6d4',
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', size: 12, weight: '600' } }
                }
            },
            scales: {
                x: {
                    ticks: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans' } },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' }
                },
                y: {
                    ticks: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans' } },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' }
                }
            }
        }
    });

    // 2d. Churn Risk by Tenure Cohort Line Chart
    const tenureCtx = document.getElementById('tenureChart').getContext('2d');
    tenureChart = new Chart(tenureCtx, {
        type: 'line',
        data: {
            labels: ['0-12 Months', '12-24 Months', '24-36 Months', '36-48 Months', '48-60 Months', '60-72 Months'],
            datasets: [{
                label: 'Churn Probability (%)',
                data: [47.5, 28.1, 20.3, 14.8, 9.2, 5.8],
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.08)',
                fill: true,
                tension: 0.4,
                borderWidth: 3,
                pointBackgroundColor: '#3b82f6',
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: document.body.classList.contains('light-theme') ? '#64748b' : '#94a3b8', font: { family: 'Outfit', size: 12, weight: '500' } }
                }
            },
            scales: {
                x: {
                    ticks: { color: document.body.classList.contains('light-theme') ? '#64748b' : '#94a3b8', font: { family: 'Outfit' } },
                    grid: { display: false }
                },
                y: {
                    ticks: { 
                        color: document.body.classList.contains('light-theme') ? '#64748b' : '#94a3b8', 
                        font: { family: 'Outfit' },
                        callback: function(value) { return value + '%'; }
                    },
                    grid: { color: document.body.classList.contains('light-theme') ? '#e2e8f0' : 'rgba(255, 255, 255, 0.05)' }
                }
            }
        }
    });

    // 2e. Model Comparison Chart (Horizontal Bar)
    const modelCtx = document.getElementById('modelComparisonChart');
    if (modelCtx) {
        modelComparisonChart = new Chart(modelCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Gradient Boosting', 'AdaBoost', 'Logistic Regression', 'Voting Classifier', 'SVM (Linear)', 'Naive Bayes', 'Kernel SVM', 'Random Forest', 'Decision Tree', 'KNN'],
                datasets: [{
                    label: 'ROC AUC Score',
                    data: [84.3, 84.1, 84.1, 84.0, 83.8, 82.7, 82.5, 82.4, 81.9, 78.8],
                    backgroundColor: [
                        '#10b981', 'rgba(16, 185, 129, 0.7)', 'rgba(16, 185, 129, 0.7)', 'rgba(16, 185, 129, 0.7)', 
                        'rgba(16, 185, 129, 0.5)', 'rgba(16, 185, 129, 0.5)', 'rgba(16, 185, 129, 0.5)', 
                        'rgba(16, 185, 129, 0.4)', 'rgba(16, 185, 129, 0.4)', 'rgba(16, 185, 129, 0.3)'
                    ],
                    borderRadius: 6,
                    borderWidth: 0,
                    barPercentage: 0.75
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) { return ` ROC AUC: ${context.parsed.x}%`; }
                        }
                    }
                },
                scales: {
                    x: {
                        min: 50,
                        max: 90,
                        ticks: { color: document.body.classList.contains('light-theme') ? '#64748b' : '#94a3b8', font: { family: 'Outfit' }, callback: function(value) { return value + '%'; } },
                        grid: { color: document.body.classList.contains('light-theme') ? '#e2e8f0' : 'rgba(255, 255, 255, 0.05)' }
                    },
                    y: {
                        ticks: { color: document.body.classList.contains('light-theme') ? '#64748b' : '#94a3b8', font: { family: 'Outfit', weight: 'bold' } },
                        grid: { display: false }
                    }
                }
            }
        });
    }

    // 2f. Monthly Charges Distribution KDE simulation (Line Chart)
    const monthlyCtx = document.getElementById('monthlyChargesDistChart');
    if (monthlyCtx) {
        monthlyChargesDistChart = new Chart(monthlyCtx.getContext('2d'), {
            type: 'line',
            data: {
                labels: ['$20', '$30', '$40', '$50', '$60', '$70', '$80', '$90', '$100', '$110', '$120'],
                datasets: [
                    {
                        label: 'Retained Customers',
                        data: [38.2, 14.5, 10.1, 8.2, 7.8, 6.5, 5.2, 4.8, 3.1, 1.4, 0.2],
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.08)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 2,
                        pointRadius: 0
                    },
                    {
                        label: 'Churned Customers',
                        data: [4.8, 6.2, 8.5, 10.1, 12.4, 15.6, 18.2, 14.5, 7.2, 2.1, 0.4],
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.08)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 2,
                        pointRadius: 0
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { color: document.body.classList.contains('light-theme') ? '#64748b' : '#94a3b8', font: { family: 'Outfit', size: 11 } }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: document.body.classList.contains('light-theme') ? '#64748b' : '#94a3b8', font: { family: 'Outfit' } },
                        grid: { display: false }
                    },
                    y: {
                        ticks: { color: document.body.classList.contains('light-theme') ? '#64748b' : '#94a3b8', font: { family: 'Outfit' }, callback: function(value) { return value + '%'; } },
                        grid: { color: document.body.classList.contains('light-theme') ? '#e2e8f0' : 'rgba(255, 255, 255, 0.05)' }
                    }
                }
            }
        });
    }

    // 2g. Services Security count plot (Grouped Bar Chart)
    const servicesCtx = document.getElementById('servicesSecurityChart');
    if (servicesCtx) {
        servicesSecurityChart = new Chart(servicesCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Security: No', 'Security: Yes', 'Support: No', 'Support: Yes'],
                datasets: [
                    {
                        label: 'Retained',
                        data: [2037, 1724, 2027, 1730],
                        backgroundColor: '#3b82f6',
                        borderRadius: 4
                    },
                    {
                        label: 'Churned',
                        data: [1461, 295, 1446, 310],
                        backgroundColor: '#ef4444',
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { color: document.body.classList.contains('light-theme') ? '#64748b' : '#94a3b8', font: { family: 'Outfit', size: 11 } }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: document.body.classList.contains('light-theme') ? '#64748b' : '#94a3b8', font: { family: 'Outfit' } },
                        grid: { display: false }
                    },
                    y: {
                        ticks: { color: document.body.classList.contains('light-theme') ? '#64748b' : '#94a3b8', font: { family: 'Outfit' } },
                        grid: { color: document.body.classList.contains('light-theme') ? '#e2e8f0' : 'rgba(255, 255, 255, 0.05)' }
                    }
                }
            }
        });
    }

    // 3. Form Submission for Prediction
    const form = document.getElementById('prediction-form');
    const resultCard = document.getElementById('prediction-result-card');
    const emptyState = resultCard.querySelector('.result-empty-state');
    const readyState = resultCard.querySelector('.result-ready-state');
    const riskCircleFill = document.getElementById('risk-circle-fill');
    const riskPercentageVal = document.getElementById('risk-percentage-val');
    const churnPredictionLabel = document.getElementById('churn-prediction-label');
    const breakdownText = document.getElementById('result-breakdown-text');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show spinner / loading logic
        emptyState.classList.add('hidden');
        readyState.classList.remove('hidden');
        
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                const prob = result.churn_probability;
                const percentage = Math.round(prob * 100);
                
                // Update Risk Meter Donut
                riskPercentageVal.textContent = `${percentage}%`;
                riskCircleFill.setAttribute('stroke-dasharray', `${percentage}, 100`);
                
                const meter = riskCircleFill.closest('.circular-chart');
                meter.classList.remove('safe', 'warning', 'danger');
                churnPredictionLabel.classList.remove('label-safe', 'label-warning', 'label-danger');

                if (prob < 0.3) {
                    meter.classList.add('safe');
                    churnPredictionLabel.textContent = 'Low Risk';
                    churnPredictionLabel.classList.add('label-safe');
                    breakdownText.innerHTML = `Customer shows high loyalty (<strong>${percentage}%</strong> risk probability). Retention action is not immediately required.`;
                } else if (prob < 0.65) {
                    meter.classList.add('warning');
                    churnPredictionLabel.textContent = 'Medium Risk';
                    churnPredictionLabel.classList.add('label-warning');
                    breakdownText.innerHTML = `Customer exhibits signs of churn risk (<strong>${percentage}%</strong> probability). Recommend value-bundle marketing incentives.`;
                } else {
                    meter.classList.add('danger');
                    churnPredictionLabel.textContent = 'High Risk';
                    churnPredictionLabel.classList.add('label-danger');
                    breakdownText.innerHTML = `Critical alert! Customer has <strong>${percentage}%</strong> probability of leaving. Transition to customer success agent immediately.`;
                }
            } else {
                breakdownText.textContent = `Error: ${result.message}`;
            }
        } catch (err) {
            breakdownText.textContent = `Network Error: ${err.message}`;
        }
    });

    // Load dynamic feature importances on page startup
    loadFeatureImportance();

    // Initialize Pearson correlation heatmap matrix
    initializeCorrelationHeatmap();
});

// 4. Load Sample Customer Demo Data helper
function loadSampleData(type) {
    const data = {
        loyal: {
            gender: 'Male',
            SeniorCitizen: '0',
            Partner: 'Yes',
            Dependents: 'Yes',
            PhoneService: 'Yes',
            MultipleLines: 'Yes',
            InternetService: 'DSL',
            OnlineSecurity: 'Yes',
            OnlineBackup: 'Yes',
            DeviceProtection: 'Yes',
            TechSupport: 'Yes',
            StreamingTV: 'No',
            StreamingMovies: 'No',
            tenure: '48',
            Contract: 'Two year',
            PaperlessBilling: 'No',
            PaymentMethod: 'Bank transfer (automatic)',
            MonthlyCharges: '55.20',
            TotalCharges: '2649.60'
        },
        churn: {
            gender: 'Female',
            SeniorCitizen: '1',
            Partner: 'No',
            Dependents: 'No',
            PhoneService: 'Yes',
            MultipleLines: 'No',
            InternetService: 'Fiber optic',
            OnlineSecurity: 'No',
            OnlineBackup: 'No',
            DeviceProtection: 'No',
            TechSupport: 'No',
            StreamingTV: 'Yes',
            StreamingMovies: 'Yes',
            tenure: '2',
            Contract: 'Month-to-month',
            PaperlessBilling: 'Yes',
            PaymentMethod: 'Electronic check',
            MonthlyCharges: '95.85',
            TotalCharges: '191.70'
        }
    };

    const profile = data[type];
    if (!profile) return;

    // Fill form elements
    Object.keys(profile).forEach(key => {
        const input = document.getElementById(key);
        if (input) {
            input.value = profile[key];
        }
    });

    // Auto-navigate to Predictor tab for executive ease
    const predictorTabLink = document.querySelector('[data-tab="predict-tab"]');
    if (predictorTabLink) {
        predictorTabLink.click();
    }
}

// 5. Trigger model training dynamically with EventSource real-time streaming
async function triggerModelTraining() {
    const btn = document.getElementById('btn-trigger-training');
    const badge = document.getElementById('active-run-badge');
    const consoleBox = document.getElementById('console-output');
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');

    btn.disabled = true;
    badge.textContent = 'RUNNING';
    badge.classList.add('running');
    statusDot.className = 'status-dot training';
    statusText.textContent = 'Pipeline Active';

    consoleBox.textContent = `[System] Retraining request sent to MLflow backend...\n`;
    consoleBox.scrollTop = consoleBox.scrollHeight;

    try {
        const response = await fetch('/train', { method: 'POST' });
        const data = await response.json();

        if (data.status === 'success') {
            consoleBox.textContent += `[System] Training process spawned. Establishing EventSource connection...\n`;
            consoleBox.scrollTop = consoleBox.scrollHeight;

            // Connect to Server-Sent Events endpoint
            const eventSource = new EventSource('/train/stream');
            
            eventSource.onmessage = async function(event) {
                const logLine = event.data;
                
                if (logLine === '[EOF]') {
                    eventSource.close();
                    
                    // Fetch updated metrics
                    const metResponse = await fetch('/metrics');
                    const metData = await metResponse.json();
                    
                    // Update stats values in UI
                    document.getElementById('metric-accuracy').textContent = `${(metData.accuracy * 100).toFixed(1)}%`;
                    document.getElementById('metric-roc-auc').textContent = `${(metData.roc_auc * 100).toFixed(1)}%`;
                    document.getElementById('metric-recall').textContent = `${(metData.recall * 100).toFixed(1)}%`;
                    document.getElementById('metric-precision').textContent = `${(metData.precision * 100).toFixed(1)}%`;
                    document.getElementById('metric-f1').textContent = `${(metData.f1 * 100).toFixed(1)}%`;

                    // Update metrics progress fills
                    const fills = document.querySelectorAll('.progress-fill');
                    if (fills.length >= 5) {
                        fills[0].style.width = `${metData.accuracy * 100}%`;
                        fills[1].style.width = `${metData.roc_auc * 100}%`;
                        fills[2].style.width = `${metData.recall * 100}%`;
                        fills[3].style.width = `${metData.precision * 100}%`;
                        fills[4].style.width = `${metData.f1 * 100}%`;
                    }

                    consoleBox.textContent += `\n\n[MLflow] Pipeline successfully finished run.\n[System] Gradient Boosting model weights saved: models/churn_model.pkl\n[System] Validation metrics successfully saved: models/metrics.json`;
                    consoleBox.scrollTop = consoleBox.scrollHeight;

                    // Reload dynamic feature importances
                    await loadFeatureImportance();

                    // Re-enable trigger button
                    btn.disabled = false;
                    badge.textContent = 'Idle';
                    badge.classList.remove('running');
                    statusDot.className = 'status-dot online';
                    statusText.textContent = 'Server Online';
                } else {
                    consoleBox.textContent += logLine + '\n';
                    consoleBox.scrollTop = consoleBox.scrollHeight;
                }
            };

            eventSource.onerror = function(err) {
                console.error("EventSource failed:", err);
                eventSource.close();
                consoleBox.textContent += `\n[Error] Log stream disconnected. Training may still run in the background. Check server console.\n`;
                consoleBox.scrollTop = consoleBox.scrollHeight;
                btn.disabled = false;
                badge.textContent = 'Idle';
                badge.classList.remove('running');
                statusDot.className = 'status-dot online';
                statusText.textContent = 'Server Online';
            };
        } else {
            consoleBox.textContent += `\n[Error] Retraining failed to start: ${data.message}`;
            btn.disabled = false;
            badge.textContent = 'Error';
            badge.classList.remove('running');
        }
    } catch (err) {
        consoleBox.textContent += `\n[Network Error] Could not connect: ${err.message}`;
        btn.disabled = false;
        badge.textContent = 'Idle';
        badge.classList.remove('running');
    }
}

// Function to load and render Feature Importance dynamically
async function loadFeatureImportance() {
    const listContainer = document.getElementById('importance-list');
    if (!listContainer) return;
    try {
        const response = await fetch('/feature_importance');
        const data = await response.json();
        
        listContainer.innerHTML = '';
        data.forEach((item, index) => {
            const featureName = item[0];
            const importanceValue = (item[1] * 100).toFixed(1);
            
            const itemHTML = `
                <div class="importance-item">
                    <span class="rank">#${index + 1}</span>
                    <span class="feat-lbl">${featureName}</span>
                    <span class="feat-val">${importanceValue}%</span>
                </div>
            `;
            listContainer.insertAdjacentHTML('beforeend', itemHTML);
        });
    } catch (err) {
        console.error('Error loading feature importances:', err);
    }
}

// Pearson correlation matrix data from notebook EDA
const correlationData = {
    features: ['Tenure', 'Monthly Chg', 'Total Chg', 'Contract', 'Security', 'Churn'],
    matrix: [
        [1.00, 0.25, 0.82, 0.67, 0.33, -0.35],   // Tenure
        [0.25, 1.00, 0.65, -0.07, 0.29, 0.19],   // Monthly Chg
        [0.82, 0.65, 1.00, 0.45, 0.41, -0.20],   // Total Chg
        [0.67, -0.07, 0.45, 1.00, 0.36, -0.40],  // Contract
        [0.33, 0.29, 0.41, 0.36, 1.00, -0.29],   // Security
        [-0.35, 0.19, -0.20, -0.40, -0.29, 1.00] // Churn
    ]
};

// Function to generate the correlation heatmap grid dynamically
function initializeCorrelationHeatmap() {
    const grid = document.getElementById('correlation-grid');
    if (!grid) return;
    
    const features = correlationData.features;
    const matrix = correlationData.matrix;
    
    grid.innerHTML = '';
    
    // Add top-left empty cell
    grid.insertAdjacentHTML('beforeend', '<div class="heatmap-cell heatmap-label-row"></div>');
    
    // Add top label row
    features.forEach(feat => {
        grid.insertAdjacentHTML('beforeend', `<div class="heatmap-cell heatmap-label-row">${feat}</div>`);
    });
    
    // Add matrix rows
    for (let r = 0; r < features.length; r++) {
        // Label column
        grid.insertAdjacentHTML('beforeend', `<div class="heatmap-cell heatmap-label-col">${features[r]}</div>`);
        
        // Heatmap cells
        for (let c = 0; c < features.length; c++) {
            const val = matrix[r][c];
            let bg;
            if (val > 0) {
                // scale warm red
                bg = `rgba(239, 68, 68, ${val * 0.8})`;
            } else {
                // scale cool blue
                bg = `rgba(59, 130, 246, ${Math.abs(val) * 0.8})`;
            }
            
            grid.insertAdjacentHTML('beforeend', `
                <div class="heatmap-cell" style="background: ${bg};" title="Correlation between ${features[r]} and ${features[c]}: ${val.toFixed(2)}">
                    ${val === 1 ? '1.0' : val.toFixed(2)}
                </div>
            `);
        }
    }
}
