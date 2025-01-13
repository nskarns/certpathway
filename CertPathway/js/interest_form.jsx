import React from 'react';
import Checkbox from '@mui/material/Checkbox';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

const InterestForm = () => {
    
    const [certificates, setCertificates] = React.useState([]);
    const [budgets, setBudgets] = React.useState([]);
    const [completionTimes, setCompletionTimes] = React.useState([]);

    const [budgetsChecked, setBudgetsChecked] = React.useState(new Array(budgets.length).fill(false));
    const [completionTimesChecked, setCompletionTimesChecked] = React.useState(new Array(completionTimes.length).fill(false));
    const [certificatesChecked, setCertificatesChecked] = React.useState(new Array(certificates.length).fill(false));

    const [otherCertificates, setOtherCertificates] = React.useState("");
    const [resume, setResume] = React.useState(null);

    const [isResultsDisabled, setIsResultsDisabled] = React.useState(true);
    const [isFormDisabled, setIsFormDisabled] = React.useState(false);

    React.useEffect(() => {
        let ignoreStaleRequest = false;
        console.log("testing")

        fetch('/api/v1/form/', { credentials: "same-origin" })
            .then(response => {
                if (!response.ok) throw Error(response.statusText);
                return response.json()
            })
            .then(data => {
                if (!ignoreStaleRequest) {
                    setCertificates(data.certificates);
                    setBudgets(data.budgets);
                    setCompletionTimes(data.completion_times);
                    if (data.budgets && data.completion_times && data.certificates) {
                        setBudgetsChecked(new Array(data.budgets.length).fill(false));
                        setCompletionTimesChecked(new Array(data.completion_times.length).fill(false));
                        setCertificatesChecked(new Array(data.certificates.length).fill(false));
                    }
                }
            })
            .catch((error) => console.log(error));

        return () => {
            ignoreStaleRequest = true;
        };
    }, []);

    function sendResume() {
        const formData = new FormData();
        formData.append('file', resume);

        console.log(formData)

        fetch('/api/v1/resume/', {
            method: 'POST',
            body: formData,
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .catch((error) => console.log(error));
    }

    function onSubmitButtonClick() {
        sendResume();

        const checkedBudgets = budgetsChecked.map((isChecked, index) => isChecked ? index : null).filter(index => index !== null);
        const checkedCompletionTimes = completionTimesChecked.map((isChecked, index) => isChecked ? index : null).filter(index => index !== null);
        const checkedCertificates = certificatesChecked.map((isChecked, index) => isChecked ? index : null).filter(index => index !== null);

        const data = {
            budgets: checkedBudgets, 
            completionTimes: checkedCompletionTimes,
            certificates: checkedCertificates,
            otherCertificates: otherCertificates,
        }
        console.log(data)

        fetch("/api/v1/form/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                setIsResultsDisabled(false);
                setIsFormDisabled(true);
            }
        })
        .catch((error) => console.log(error));
    }

    return (
        <div>
            <h1>Interest Form</h1>
            <h3>Welcome to CertPathway!</h3>

            <p>What types of certificate are you interested in pursuing? (you may select multiple)</p>
            {certificates.map((certificate, index) => (
                <div key={index}>
                    <Checkbox 
                        name={certificate} 
                        value={certificate}
                        checked={certificatesChecked[index]}
                        disabled={isFormDisabled}
                        onChange={() => {
                            const newCertificatesChecked = [...certificatesChecked];
                            newCertificatesChecked[index] = !newCertificatesChecked[index];
                            setCertificatesChecked(newCertificatesChecked);
                        }}
                        
                    />
                    <label>{certificate}</label>
                </div>
            ))}

            <p>Do you have any other certificates? (optional)
                <br/>Format: <i>Name of certificate, Providing/Sponsoring Organization</i>
                <br/>Ex: <i>Certified Medical Assistant, American Association of Medical Assistants</i>
            </p>
            <TextField 
                multiline 
                rows={4} 
                variant="outlined" 
                name="other_certificates" 
                disabled={isFormDisabled}
                onChange={(event) => setOtherCertificates(event.target.value)} 
            />

            <p>What is your budget range? (you may select multiple)</p>
            {budgets.map((budget, index) => (
                <div key={index}>
                    <Checkbox 
                        name="budget" 
                        value={budget}
                        checked={budgetsChecked[index]} 
                        disabled={isFormDisabled}
                        onChange={() => {
                            const newBudgetsChecked = [...budgetsChecked];
                            newBudgetsChecked[index] = !newBudgetsChecked[index];
                            setBudgetsChecked(newBudgetsChecked); 
                        }}
                    />
                    <label>{budget}</label>
                </div>
            ))}

            <p>What is your range for time of completion? (you may select multiple)</p>
            {completionTimes.map((time, index) => (
                <div key={index}>
                    <Checkbox 
                        name="time" 
                        value={time} 
                        checked={completionTimesChecked[index]} 
                        disabled={isFormDisabled}
                        onChange={() => {
                            const newCompletionTimesChecked = [...completionTimesChecked];
                            newCompletionTimesChecked[index] = !newCompletionTimesChecked[index];
                            setCompletionTimesChecked(newCompletionTimesChecked);
                        }} 
                    />
                    <label>{time}</label>
                </div>
            ))}

            <p>Upload Resume (optional)</p>
            <input 
                type="file" 
                name="file" 
                accept="application/pdf" 
                disabled={isFormDisabled}
                onChange={(event) => setResume(event.target.files[0])} 
            />

            <Button 
                variant="contained" 
                color="primary" 
                type="submit" 
                name="operation" 
                value="create" 
                disabled={isFormDisabled}
                onClick={() => onSubmitButtonClick()}
            >
                Submit Information
            </Button>

            <Button 
                variant="text" 
                color="primary"
                href="/explore/"
                disabled={isResultsDisabled}
            >
                See Results
            </Button>

        </div>
    );
};

export default InterestForm;