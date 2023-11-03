import streamlit as st
from web3 import Web3
import dotenv

dotenv.load_dotenv()

# Connect to local Ethereum node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Ensure connected to Ethereum
if not w3.is_connected():
    st.error("Failed to connect to Ethereum")
    st.stop()

# Loading contract details
CONTRACT_ABI = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			}
		],
		"name": "createStudentProfile",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			}
		],
		"name": "createUniversityProfile",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_studentId",
				"type": "uint256"
			}
		],
		"name": "getCertificates",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_studentId",
				"type": "uint256"
			}
		],
		"name": "isStudent",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_address",
				"type": "address"
			}
		],
		"name": "isUniversity",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_studentId",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_cert",
				"type": "string"
			}
		],
		"name": "issueCertificate",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "studentCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "studentProfiles",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "studentId",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "exists",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "universityProfiles",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "exists",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
CONTRACT_ADDRESS = "0x8d94c21348cB71E2E8B1d9d25Ee0bcE4F1D6C92b"
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
# Connect to local Ethereum node
# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Set the default account
if len(w3.eth.accounts) > 0:
    w3.eth.defaultAccount = w3.eth.accounts[0]
else:
    st.error("No Ethereum accounts found. Please create an account first.")
    st.stop()

st.title("Education Credentials on Blockchain")

# Sign Up as University or Student
role = st.selectbox("Choose your role:", ["University", "Student", "Viewer"])

if role == "University":
    uni_name = st.text_input("Enter University Name:")
    if st.button("Sign Up as University"):
        tx_hash = contract.functions.createUniversityProfile(uni_name).transact()
        st.success(f"University profile created with transaction hash: {tx_hash.hex()}")

elif role == "Student":
    student_name = st.text_input("Enter Student Name:")
    if st.button("Sign Up as Student"):
        tx_hash = contract.functions.createStudentProfile(student_name).transact()
        st.success(f"Student profile created with transaction hash: {tx_hash.hex()}")

    student_id = st.text_input("Enter your Student ID to see your certificates:")
    if st.button("View My Certificates"):
        # You will need to implement this functionality in the contract. As of now, assuming there's a function called `getCertificatesForStudent`.
        certificates = contract.functions.getCertificatesForStudent(student_id).call()
        st.write(certificates)

elif role == "Viewer":
    student_id_to_view = st.text_input("Enter Student ID to view their certificates:")
    if st.button("View Certificates"):
        # Assuming same function for retrieval as mentioned above.
        certificates = contract.functions.getCertificatesForStudent(student_id_to_view).call()
        st.write(certificates)

# Issue Certificate
student_address = st.text_input("Enter Student's Ethereum Address to Issue Certificate:")
certificate_details = st.text_area("Enter Certificate Details:")
if st.button("Issue Certificate"):
    tx_hash = contract.functions.issueCertificate(student_address, certificate_details).transact()
    st.success(f"Certificate issued with transaction hash: {tx_hash.hex()}")
