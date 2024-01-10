//import React from 'react';
import {useDropzone} from 'react-dropzone';
import 'bootstrap/dist/css/bootstrap.css';
import toast from 'react-hot-toast';

declare module 'react' {
  interface InputHTMLAttributes<T> extends HTMLAttributes<T> {
    directory?: string;
    webkitdirectory?: string;
  }
}

function ImportAndPrepareTestDataButton() {
  const {acceptedFiles, getRootProps, getInputProps} = useDropzone({
    getFilesFromEvent: event => getFiles(event)
  });

  const handleSendTrainingFiles = async () => {
    const uploadEndpoint = 'http://localhost:5000/upload_and_prepare_training_files';
    toast.loading("Importing and preparing files.");
  
    const formData = new FormData();
    acceptedFiles.forEach(file => {
      formData.append('file', file);
    });

    try {
    const response = await fetch(uploadEndpoint, {
        method: 'POST',
        body: formData,
    });

    if (response.ok) {
        const data = await response.json();
        toast.dismiss();
        toast.success(`Successfully imported ${data.num_processed_and_writen_instance} files.`, {
          duration: 3000
        });
    } else {
        console.error('Error while uploading and preparing files:', response.statusText);
        toast.dismiss();
        toast.error('Error while uploading and preparing files.');
    }
    } catch (error) {
    console.error('Error while uploading and preparing files:', error);
    toast.dismiss();
    toast.error('Error while uploading and preparing files.');
    }
  };

  return (
    <div className="btn-group mx-5">
      <div {...getRootProps({className: 'btn btn-outline-primary dropzone', type:'button'})}>
        <input {...getInputProps()} directory="" webkitdirectory="" type="file"/>
        <div className="d-flex justify-content-center align-items-center text-center">
          <p className="w-100 mb-0">Click To Select Files</p>
        </div>
      </div>
      <button type="button" className="btn btn-outline-primary" onClick={handleSendTrainingFiles}>Import And Prepare Test Data</button>
    </div>
  );
}

async function getFiles(event: any) {
  const files = [];
  const fileList = event.dataTransfer ? event.dataTransfer.files : event.target.files;

  for (var i = 0; i < fileList.length; i++) {
    const file = fileList.item(i);
    
    Object.defineProperty(file, 'myProp', {
      value: true
    });

    files.push(file);
  }

  return files;
}

export default ImportAndPrepareTestDataButton;
