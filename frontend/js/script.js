`'javascript
document.addEventListener("DOMContentLoaded", function () {

    const chatInput = document.getElementById("chatInput");
    const sendButton = document.getElementById("sendButton");
    const conversation = document.querySelector(".conversation");

    // =========================
    // CHECK ELEMENTS
    // =========================

    if (!chatInput || !sendButton || !conversation) {
        console.error("Nuvexa AI: Chat elements not found.");
        return;
    }

    // =========================
    // LEAD CAPTURE STATE
    // =========================

    let leadState = null;

    let leadData = {
        name: "",
        phone: "",
        course: "",
        enquiry: ""
    };

    // =========================
    // ADD MESSAGE TO CHAT
    // =========================

    function addMessage(message, type) {

        const messageDiv = document.createElement("div");

        messageDiv.className =
            type === "user"
                ? "user-message"
                : "ai-message";

        messageDiv.textContent = message;

        conversation.appendChild(messageDiv);

        conversation.scrollTop =
            conversation.scrollHeight;
    }

    // =========================
    // CHECK LEAD INTENT
    // =========================

    function isLeadIntent(message) {

        const text = message.toLowerCase();

        const keywords = [
            "join",
            "admission",
            "admission lena",
            "course lena",
            "course join",
            "enroll",
            "enrollment",
            "demo",
            "free demo",
            "interested",
            "apply",
            "registration",
            "register",
            "seekhna hai",
            "lena hai",
            "karna hai"
        ];

        return keywords.some(function (keyword) {
            return text.includes(keyword);
        });
    }

    // =========================
    // SAVE LEAD
    // =========================

    async function saveLead() {

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/leads",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        name: leadData.name,
                        phone: leadData.phone,
                        course: leadData.course,
                        enquiry:
                            leadData.enquiry ||
                            "Customer enquiry"
                    })
                }
            );

            if (!response.ok) {
                throw new Error(
                    "Lead API Error: " + response.status
                );
            }

            const data = await response.json();

            console.log(
                "Lead saved successfully:",
                data
            );

            addMessage(
                "Thank you! 🎉 Aapki details successfully save ho gayi hain. Hamari team aapse jaldi contact karegi.",
                "ai"
            );

        } catch (error) {

            console.error(
                "Lead Save Error:",
                error
            );

            addMessage(
                "Sorry, lead save karne mein problem aa gayi. Please thodi der baad try karein.",
                "ai"
            );
        }

        // Reset lead state

        leadState = null;

        leadData = {
            name: "",
            phone: "",
            course: "",
            enquiry: ""
        };
    }

    // =========================
    // HANDLE LEAD CONVERSATION
    // =========================

    async function handleLeadCapture(message) {

        // STEP 1 - NAME

        if (leadState === "name") {

            leadData.name = message;

            leadState = "phone";

            addMessage(
                "Nice to meet you, " +
                leadData.name +
                " 😊\n\nAapka mobile number bata dijiye.",
                "ai"
            );

            return true;
        }

        // STEP 2 - PHONE

        if (leadState === "phone") {

            const phone = message.replace(/\D/g, "");

            if (phone.length !== 10) {

                addMessage(
                    "Please apna valid 10-digit mobile number enter karein.",
                    "ai"
                );

                return true;
            }

            leadData.phone = phone;

            leadState = "course";

            addMessage(
                "Great 👍\n\nAap kis course mein interested hain?",
                "ai"
            );

            return true;
        }

        // STEP 3 - COURSE

        if (leadState === "course") {

            leadData.course = message;

            await saveLead();

            return true;
        }

        return false;
    }

    // =========================
    // SEND MESSAGE
    // =========================

    async function sendMessage() {

        const message = chatInput.value.trim();

        if (message === "") {
            return;
        }

        // Disable button while processing

        sendButton.disabled = true;

        // Show user message

        addMessage(
            message,
            "user"
        );

        // Clear input

        chatInput.value = "";

        // =========================
        // LEAD FLOW
        // =========================

        if (leadState !== null) {

            await handleLeadCapture(message);

            sendButton.disabled = false;

            chatInput.focus();

            return;
        }

        // =========================
        // CHECK CUSTOMER INTEREST
        // =========================

        if (isLeadIntent(message)) {

            leadData.enquiry = message;

            leadState = "name";

            addMessage(
                "Bilkul! 😊 Main aapki enquiry ke liye details note kar leta hoon.\n\nAapka naam kya hai?",
                "ai"
            );

            sendButton.disabled = false;

            chatInput.focus();

            return;
        }

        // =========================
        // NORMAL AI CHAT
        // =========================

        const aiMessage =
            document.createElement("div");

        aiMessage.className =
            "ai-message";

        aiMessage.textContent =
            "Nuvexa AI is thinking... 🤖";

        conversation.appendChild(
            aiMessage
        );

        conversation.scrollTop =
            conversation.scrollHeight;

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );

            if (!response.ok) {

                throw new Error(
                    "HTTP Error: " +
                    response.status
                );
            }

            const data =
                await response.json();

            console.log(
                "AI Response:",
                data
            );

            // Backend may return either key

            const aiResponse =
                data.ai_response ||
                data.response;

            if (!aiResponse) {

                throw new Error(
                    "AI response not received"
                );
            }

            // Show AI response

            aiMessage.textContent =
                aiResponse;

            conversation.scrollTop =
                conversation.scrollHeight;

        } catch (error) {

            console.error(
                "Nuvexa AI Chat Error:",
                error
            );

            aiMessage.textContent =
                "Sorry, Nuvexa AI is currently unavailable.";
        }

        // Enable button

        sendButton.disabled = false;

        chatInput.focus();
    }

    // =========================
    // SEND BUTTON
    // =========================

    sendButton.addEventListener(
        "click",
        sendMessage
    );

    // =========================
    // ENTER KEY
    // =========================

    chatInput.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Enter") {

                event.preventDefault();

                sendMessage();
            }
        }
    );

});
```