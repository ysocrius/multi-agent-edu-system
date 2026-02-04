// API endpoint
const API_URL = '/api/generate';

// DOM elements
const form = document.getElementById('contentForm');
const generateBtn = document.getElementById('generateBtn');
const pipelineSection = document.getElementById('pipelineSection');
const errorBox = document.getElementById('errorBox');

// Form submission handler
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const grade = parseInt(document.getElementById('grade').value);
    const topic = document.getElementById('topic').value.trim();
    
    if (!grade || !topic) {
        showError('Please fill in all fields');
        return;
    }
    
    await generateContent(grade, topic);
});

// Main content generation function
async function generateContent(grade, topic) {
    try {
        // Reset UI
        resetPipeline();
        hideError();
        showPipeline();
        
        // Disable form
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        
        // Stage 1: Generator - In Progress
        updateStageStatus(1, 'in-progress', 'Generating...');
        
        // Call API
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ grade, topic })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'API request failed');
        }
        
        const data = await response.json();
        
        // Stage 1: Generator - Complete
        updateStageStatus(1, 'complete', 'Complete');
        displayGeneratorOutput(data.generator_output, 'content1', 'explanation1', 'mcqs1');
        showStageContent(1);
        
        await sleep(500);
        
        // Stage 2: Reviewer - In Progress
        updateStageStatus(2, 'in-progress', 'Evaluating...');
        
        await sleep(1000);
        
        // Stage 2: Reviewer - Complete
        const reviewStatus = data.reviewer_feedback.status;
        if (reviewStatus === 'pass') {
            updateStageStatus(2, 'complete', 'Passed');
            displayReviewResult('pass', data.reviewer_feedback.feedback);
        } else {
            updateStageStatus(2, 'needs-revision', 'Needs Revision');
            displayReviewResult('fail', data.reviewer_feedback.feedback);
        }
        showStageContent(2);
        
        await sleep(500);
        
        // Stage 3: Refinement (if occurred)
        if (data.refinement_occurred) {
            showStage(3);
            updateStageStatus(3, 'in-progress', 'Refining...');
            
            await sleep(1000);
            
            updateStageStatus(3, 'complete', 'Complete');
            showStageContent(3);
            
            await sleep(500);
        }
        
        // Display final output
        displayFinalOutput(data.final_output);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        // Re-enable form
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate Content';
    }
}

// UI Update Functions
function updateStageStatus(stageNum, status, text) {
    const badge = document.getElementById(`status${stageNum}`);
    const stage = document.getElementById(`stage${stageNum}`);
    
    // Remove all status classes
    badge.classList.remove('pending', 'in-progress', 'complete', 'needs-revision');
    stage.classList.remove('active', 'success', 'warning');
    
    // Add new status
    badge.classList.add(status);
    badge.textContent = text;
    
    // Update stage styling
    if (status === 'in-progress') {
        stage.classList.add('active');
    } else if (status === 'complete') {
        stage.classList.add('success');
    } else if (status === 'needs-revision') {
        stage.classList.add('warning');
    }
}

function showStageContent(stageNum) {
    document.getElementById(`content${stageNum}`).classList.remove('hidden');
}

function showStage(stageNum) {
    document.getElementById(`stage${stageNum}`).classList.remove('hidden');
}

function displayGeneratorOutput(output, contentId, explanationId, mcqsId) {
    // Display explanation
    document.getElementById(explanationId).textContent = output.explanation;
    
    // Display MCQs
    const mcqsContainer = document.getElementById(mcqsId);
    mcqsContainer.innerHTML = '';
    
    output.mcqs.forEach((mcq, index) => {
        const mcqDiv = document.createElement('div');
        mcqDiv.className = 'mcq-item';
        
        const question = document.createElement('div');
        question.className = 'mcq-question';
        question.textContent = `Q${index + 1}: ${mcq.question}`;
        
        const options = document.createElement('ul');
        options.className = 'mcq-options';
        mcq.options.forEach((opt, i) => {
            const li = document.createElement('li');
            li.textContent = `${String.fromCharCode(65 + i)}. ${opt}`;
            options.appendChild(li);
        });
        
        const answer = document.createElement('div');
        answer.className = 'mcq-answer';
        answer.textContent = `✓ Correct Answer: ${mcq.answer}`;
        
        mcqDiv.appendChild(question);
        mcqDiv.appendChild(options);
        mcqDiv.appendChild(answer);
        mcqsContainer.appendChild(mcqDiv);
    });
}

function displayReviewResult(status, feedback) {
    const resultDiv = document.getElementById('reviewResult');
    const feedbackBox = document.getElementById('feedbackBox');
    const feedbackList = document.getElementById('feedbackList');
    
    if (status === 'pass') {
        resultDiv.innerHTML = '<p style="color: #28a745; font-weight: 600;">✅ Content passed all quality checks!</p>';
        feedbackBox.classList.add('hidden');
    } else {
        resultDiv.innerHTML = '<p style="color: #ffc107; font-weight: 600;">⚠️ Content needs revision</p>';
        
        // Display feedback
        feedbackList.innerHTML = '';
        feedback.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            feedbackList.appendChild(li);
        });
        
        feedbackBox.classList.remove('hidden');
    }
}

function displayFinalOutput(output) {
    const finalSection = document.getElementById('finalOutput');
    
    // Display explanation
    document.getElementById('finalExplanation').textContent = output.explanation;
    
    // Display MCQs
    const mcqsContainer = document.getElementById('finalMcqs');
    mcqsContainer.innerHTML = '';
    
    output.mcqs.forEach((mcq, index) => {
        const mcqDiv = document.createElement('div');
        mcqDiv.className = 'mcq-item';
        
        const question = document.createElement('div');
        question.className = 'mcq-question';
        question.textContent = `Q${index + 1}: ${mcq.question}`;
        
        const options = document.createElement('ul');
        options.className = 'mcq-options';
        mcq.options.forEach((opt, i) => {
            const li = document.createElement('li');
            li.textContent = `${String.fromCharCode(65 + i)}. ${opt}`;
            options.appendChild(li);
        });
        
        const answer = document.createElement('div');
        answer.className = 'mcq-answer';
        answer.textContent = `✓ Correct Answer: ${mcq.answer}`;
        
        mcqDiv.appendChild(question);
        mcqDiv.appendChild(options);
        mcqDiv.appendChild(answer);
        mcqsContainer.appendChild(mcqDiv);
    });
    
    finalSection.classList.remove('hidden');
    
    // Scroll to final output
    finalSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showPipeline() {
    pipelineSection.classList.remove('hidden');
}

function resetPipeline() {
    // Reset all stages
    for (let i = 1; i <= 3; i++) {
        updateStageStatus(i, 'pending', 'Pending');
        document.getElementById(`content${i}`).classList.add('hidden');
        
        const stage = document.getElementById(`stage${i}`);
        stage.classList.remove('active', 'success', 'warning');
    }
    
    // Hide stage 3 and final output
    document.getElementById('stage3').classList.add('hidden');
    document.getElementById('finalOutput').classList.add('hidden');
}

function showError(message) {
    errorBox.textContent = `Error: ${message}`;
    errorBox.classList.remove('hidden');
}

function hideError() {
    errorBox.classList.add('hidden');
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
