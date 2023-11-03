// Connect to Ethereum with Web3.js
let web3;
if (typeof web3 !== "undefined") {
  web3 = new Web3(web3.currentProvider);
} else {
  // Connect to local node
  web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
}

// Contract ABI and Address
const contractABI = [
  [
    {
      inputs: [],
      name: "certificateCounter",
      outputs: [
        {
          internalType: "uint256",
          name: "",
          type: "uint256",
        },
      ],
      stateMutability: "view",
      type: "function",
    },
    {
      inputs: [
        {
          internalType: "uint256",
          name: "",
          type: "uint256",
        },
      ],
      name: "certificates",
      outputs: [
        {
          internalType: "address",
          name: "university",
          type: "address",
        },
        {
          internalType: "address",
          name: "student",
          type: "address",
        },
        {
          internalType: "string",
          name: "certificateData",
          type: "string",
        },
        {
          internalType: "uint256",
          name: "timestamp",
          type: "uint256",
        },
      ],
      stateMutability: "view",
      type: "function",
    },
    {
      inputs: [
        {
          internalType: "string",
          name: "_profileData",
          type: "string",
        },
      ],
      name: "createStudentProfile",
      outputs: [],
      stateMutability: "nonpayable",
      type: "function",
    },
    {
      inputs: [
        {
          internalType: "string",
          name: "_profileData",
          type: "string",
        },
      ],
      name: "createUniversityProfile",
      outputs: [],
      stateMutability: "nonpayable",
      type: "function",
    },
    {
      inputs: [
        {
          internalType: "uint256",
          name: "_certificateId",
          type: "uint256",
        },
      ],
      name: "getCertificate",
      outputs: [
        {
          internalType: "address",
          name: "",
          type: "address",
        },
        {
          internalType: "address",
          name: "",
          type: "address",
        },
        {
          internalType: "string",
          name: "",
          type: "string",
        },
        {
          internalType: "uint256",
          name: "",
          type: "uint256",
        },
      ],
      stateMutability: "view",
      type: "function",
    },
    {
      inputs: [
        {
          internalType: "address",
          name: "_student",
          type: "address",
        },
        {
          internalType: "string",
          name: "_certificateData",
          type: "string",
        },
      ],
      name: "issueCertificate",
      outputs: [],
      stateMutability: "nonpayable",
      type: "function",
    },
    {
      inputs: [
        {
          internalType: "address",
          name: "",
          type: "address",
        },
      ],
      name: "studentProfiles",
      outputs: [
        {
          internalType: "string",
          name: "",
          type: "string",
        },
      ],
      stateMutability: "view",
      type: "function",
    },
    {
      inputs: [
        {
          internalType: "address",
          name: "",
          type: "address",
        },
      ],
      name: "universityProfiles",
      outputs: [
        {
          internalType: "string",
          name: "",
          type: "string",
        },
      ],
      stateMutability: "view",
      type: "function",
    },
  ],
]; // Replace with your contract's ABI
const contractAddress = "0x6Ae7708B8f9778FDaD9b47782ee31F9ca1aE36C0"; // Replace with your contract's address
const contract = new web3.eth.Contract(contractABI, contractAddress);

// Create University Profile
async function createUniversity() {
  const uniName = document.getElementById("uniName").value;
  const accounts = await web3.eth.getAccounts();

  contract.methods
    .createUniversityProfile(uniName)
    .send({ from: accounts[0] })
    .on("confirmation", function (confirmationNumber, receipt) {
      console.log("University profile created.");
    })
    .on("error", console.error);
}

// Create Student Profile
async function createStudent() {
  const studentName = document.getElementById("studentName").value;
  const accounts = await web3.eth.getAccounts();

  contract.methods
    .createStudentProfile(studentName)
    .send({ from: accounts[0] })
    .on("confirmation", function (confirmationNumber, receipt) {
      console.log("Student profile created.");
    })
    .on("error", console.error);
}

// Issue Certificate to Student
async function issueCertificate() {
  const studentAddress = document.getElementById("studentAddress").value;
  const certificateDetails =
    document.getElementById("certificateDetails").value;
  const accounts = await web3.eth.getAccounts();

  contract.methods
    .issueCertificate(studentAddress, certificateDetails)
    .send({ from: accounts[0] })
    .on("confirmation", function (confirmationNumber, receipt) {
      console.log("Certificate issued.");
    })
    .on("error", console.error);
}

// Check Certificate Details using Certificate ID
async function checkCertificate() {
  const certId = document.getElementById("certId").value;

  contract.methods
    .getCertificateDetails(certId)
    .call()
    .then(function (details) {
      document.getElementById("certificateOutput").innerText =
        JSON.stringify(details);
    })
    .catch(console.error);
}
