import React, { useState } from 'react';
import axios from 'axios'
import { split, useQuery, useSubscription, ApolloClient, InMemoryCache, HttpLink, ApolloProvider } from '@apollo/client';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';
import gql from 'graphql-tag';
import { getMainDefinition } from '@apollo/client/utilities';

import './Grid.css';


const gridContainer = {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gridTemplateRows: 'repeat(2, 1fr)'
}

const httplink = new HttpLink({
    uri: 'http://127.0.0.1:8100/grapgql'
})

const wsLink = new GraphQLWsLink(createClient({
    url: 'ws://127.0.0.1:8100/messages',
}));

const splitLink = split(
    ({ query }) => {
        const definition = getMainDefinition(query);
        return (
            definition.kind === 'OperationDefinition' &&
            definition.operation === 'subscription'
        );
    },
    wsLink,
    httplink,
)

const client = new ApolloClient({
    cache: new InMemoryCache(),
    link: splitLink
});

const SUBSCRIPTION_QUERY = gql`
    subscription onMsgSent{
      processed_cnt_msg {
        animal_processed
        number_processed
      }
    }
  `;

function AnimalMessageList() {
    const { data, loading, error } = useSubscription(SUBSCRIPTION_QUERY, {
      shouldResubscribe: true,
    });
  
  
    if (loading) {
      return <p>Loading...</p>;
    }
  
    if (error) {
      return <p>Error: {error.message}</p>;
    }
    console.log(data)
  
    return (
      <ul>
        {/* {data.messages.map((message) => (
            <p>
              {message.content}
            </p>
        ))} */}
      </ul>
    );
  }

const Grid = () => {
    const [animalFile, setAnimalFile] = useState(null)
    const [numberFile, setNumberFile] = useState(null)

    const handleAnimalChange = (event) => {
        event.preventDefault()
        console.log("animal file uploaded")
        setAnimalFile(event.target.files[0])
    }

    const handleNumberChange = (event) => {
        event.preventDefault()
        setNumberFile(event.target.files[0])
    }

    const handleUploadAnimalAssignment = async (ev) => {
        ev.preventDefault();
        const data = new FormData();
        data.append('file', animalFile);
        data.append('job_type', "animal")
        axios.post('http://localhost:8001/upload', data).then(response => {
            console.log(response.data)
        })
    }

    const handleUploadNumberAssignment = async (ev) => {
        ev.preventDefault();

        const data = new FormData();
        data.append('file', numberFile);
        data.append('job_type', "number")
        axios.post('http://localhost:8001/upload', data).then(response => {
            console.log(response.data)
        })
        
    }
    return (   
        <div className="App">
            <header className="App-header">
                <p>
                    IDunno: A Distributed Machine Learning platform
                </p>
            </header>

            <body className="App-body">
                <div style={gridContainer}>
                    <div style={{ gridColumn: '1 / 2', gridRow: '1 / 2' }}>
                        <form onSubmit={handleUploadAnimalAssignment}>
                            <h2>Animal</h2>
                            <div>
                                <input type="file" onChange={handleAnimalChange} />
                            </div>
                            <br />
                            <div>
                                <button>Upload</button>
                            </div>
                        </form>
                    </div>
                    <div style={{ gridColumn: '2 / 3', gridRow: '1 / 2' }}>
                        <ApolloProvider client={client}>
                            <AnimalMessageList />
                        </ApolloProvider>
                    </div>
                    <div style={{ gridColumn: '3 / 4', gridRow: '1 / 2' }}>
                        <form onSubmit={handleUploadNumberAssignment}>
                            <h2>Number</h2>
                            <div>
                                <input type="file" onChange={handleNumberChange} />
                            </div>
                            <br />
                            <div>
                                <button>Upload</button>
                            </div>
                        </form>
                    </div>
                    <div style={{ gridColumn: '4 / ', gridRow: '1 / 2' }}>
                        {/* displaying the statistics for Number job*/}
                    </div>
                    <div style={{ gridColumn: '1 / 3', gridRow: '2 / 3' }}>Content for columns 1-4</div>
                    <div style={{ gridColumn: '3 / 5', gridRow: '2 / 3' }}>Content for columns 5-8</div>
                </div>
            </body>

            <footer className="App-footer">
                <p>
                    <i>Copyright: Dingsen Shi & Ruipeng Min</i>
                </p>
                <a
                    className="App-link"
                    href="https://github.com/dingsen2/IDunno"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Learn more
                </a>
                
            </footer>

        </div>
           
    );
}

export default Grid;
