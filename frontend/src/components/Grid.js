import React from 'react';

const gridContainer = {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gridTemplateRows: 'repeat(2, 1fr)'
}

const AnimalForm = (props) => {
    return (
        <form onSubmit={props.onSubmit}>
            <h2>Animal Job</h2>
            <div>
                <input type="file" name='animal_form' />
            </div>
            <br />
            <div>
                <button>Upload</button>
            </div>
        </form>
    );
}

const NumberForm = (props) => {
    return (
        <form onSubmit={props.onSubmit}>
            <h2>Number Job</h2>
            <div>
                <input type="file" name='number_form' />
            </div>
            <br />
            <div>
                <button>Upload</button>
            </div>
        </form>
    );
}


const Grid = () => {
    const handleUploadAnimalAssignment = async (job_type, ev) => {
        ev.preventDefault();
        console.log(job_type)
        const data = new FormData();
        data.append('file', this.uploadInputAnimal.files[0]);
        data.append('job_type', job_type)
        await fetch('http://localhost:8000/upload', { method: 'POST', body: data })
            .then((response) => {
                response.json().then((body) => {
                });
            });
    }

    const handleUploadNumberAssignment = async (job_type, ev) => {
        ev.preventDefault();
    
        const data = new FormData();
        data.append('file', this.uploadInputNumber.files[0]);
        data.append('job_type', job_type)
        await fetch('http://localhost:8000/upload', { method: 'POST', body: data })
            .then((response) => {
                response.json().then((body) => {
                });
            });
    }
    return (
        <div style={gridContainer}>
            <div style={{ gridColumn: '1 / 2', gridRow: '1 / 2' }}>
                <form>
                    <AnimalForm onSubmit={handleUploadAnimalAssignment.bind("animal")}/>
                </form>
            </div>
            <div style={{ gridColumn: '2 / 3', gridRow: '1 / 2' }}>
                {/* displaying the statistics for Animal job*/}
                
            </div>
            <div style={{ gridColumn: '3 / 4', gridRow: '1 / 2' }}>
                <form>
                    <NumberForm onSubmit={handleUploadNumberAssignment.bind("number")}/>
                </form>
            </div>
            <div style={{ gridColumn: '4 / ', gridRow: '1 / 2' }}>
                {/* displaying the statistics for Number job*/}
            </div>
            <div style={{ gridColumn: '1 / 3', gridRow: '2 / 3' }}>Content for columns 1-3, row 2</div>
            <div style={{ gridColumn: '3 / 5', gridRow: '2 / 3' }}>Content for columns 3-5, row 2</div>
        </div>
    );
}

export default Grid;
