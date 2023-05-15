function deleteSummary(summaryId) {
    fetch('/delete-summary', {
        method: 'POST',
        body: JSON.stringify({summaryId: summaryId})
    }).then((_res) => {
        window.location.href = '/';
    })
}