import axios from 'axios';

export  async function handler(req, res) {
    const data = await axios.get('http://localhost:8000/');
    console.log(data)
    res.status(200).json(data.data);
  }
  
export default function Home({ data }) {
    return (
      <div>
        <h1>Data from Flask backend:</h1>
        <p>{JSON.stringify(data)}</p>
      </div>
    );
  }
  export async function getStaticProps() {
    const { data } = await axios.get('http://localhost:8000/');
    return { props: { data } };
  }
  

