import React from 'react'

class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            imageURL: "",
        };
        this.handleUploadAnimalAssignment = this.handleUploadAnimalAssignment.bind(this);
        this.handleUploadNumberAssignment = this.handleUploadNumberAssignment.bind(this);
    }

    async handleUploadAnimalAssignment(job_type, ev) {
        ev.preventDefault();
        console.log(job_type)
        const data = new FormData();
        data.append('file', this.uploadInputAnimal.files[0]);
        data.append('job_type', job_type)
        await fetch('http://localhost:8001/upload', { method: 'POST', body: data })
        .then((response) => { response.json().then((body) => { 
          });
        });
      }
    
    async handleUploadNumberAssignment(job_type, ev) {
        ev.preventDefault();

        const data = new FormData();
        data.append('file', this.uploadInputNumber.files[0]);
        data.append('job_type', job_type)
        await fetch('http://localhost:8001/upload', { method: 'POST', body: data })
        .then((response) => { response.json().then((body) => { 
          });
        });
      }

    render() {
        const leftSection = (
          <form onSubmit={this.handleUploadAnimalAssignment.bind(this, "Animal")} style={{width:"50%", height:"100%"}}>
            <h2>Animal Job</h2>
            <div>
              <input ref={(ref) => { this.uploadInputAnimal = ref; }} type="file" name='animal_form' />
            </div>
            <br />
            <div>
              <button>Upload</button>
            </div>
          </form>
        );
        const rightSection = (
          <form onSubmit={this.handleUploadNumberAssignment.bind(this, "Number")} style={{width:"50%", height:"100%"}}>
            <h2>Number Job</h2>
            <div>
              <input ref={(ref) => { this.uploadInputNumber = ref; }} type="file" name='number_form' />
            </div>
            <br />
            <div>
              <button>Upload</button>
            </div>
          </form>
        );
        return (
          <div style={{ display: "flex" }}>
            {leftSection}
            {rightSection}
          </div>
        );
      }
}

export default Main;