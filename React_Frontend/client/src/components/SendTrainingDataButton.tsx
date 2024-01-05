//import React from 'react';
import {useDropzone} from 'react-dropzone';
import 'bootstrap/dist/css/bootstrap.css';

declare module 'react' {
  interface InputHTMLAttributes<T> extends HTMLAttributes<T> {
    directory?: string;
    webkitdirectory?: string;
  }
}

function SendTrainingDataButton() {
  const {acceptedFiles, getRootProps, getInputProps} = useDropzone({
    getFilesFromEvent: event => getFiles(event)
  });

  /*const files = acceptedFiles.map(f => (
    <li key={f.name}>
      {f.name}
    </li>
  ));*/

  const handleSendTrainingFiles = async () => {
    const uploadEndpoint = 'http://localhost:5000/uploadTrainingFiles';

    const formData = new FormData();
    acceptedFiles.forEach(file => {
      formData.append('file', file);
    });
    const formDataChunks = splitFormData(formData);

    for(let i = 0; i < 10; i++)
    {
      try {
        const response = await fetch(uploadEndpoint, {
          method: 'POST',
          body: formDataChunks[i],
        });
  
        if (response.ok) {
          const data = await response.json();
          console.log(data);
        } else {
          console.error('Error uploading files:', response.statusText);
        }
      } catch (error) {
        console.error('Error uploading files:', error);
      }
    }
  };

  return (
    <div className="btn-group">
      <div {...getRootProps({className: 'btn btn-outline-primary dropzone', type:'button'})}>
        <input {...getInputProps()} directory="" webkitdirectory="" type="file"/>
        <div className="d-flex justify-content-center align-items-center text-center">
          <p className="w-100 mb-0">Click To Select Files</p>
        </div>
      </div>
      <button type="button" className="btn btn-outline-primary" onClick={handleSendTrainingFiles}>Send Training Data</button>
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

function splitFormData(formData: FormData): FormData[] {
  const entries: [string, FormDataEntryValue][] = [];
  
  formData.forEach((value, key) => {
    entries.push([key, value]);
  });

  const filesPerGroup = Math.ceil(entries.length / 10);

  const groups: [string, FormDataEntryValue][][] = Array.from({ length: 10 }, (_, groupIndex) => {
    const start = groupIndex * filesPerGroup;
    const end = start + filesPerGroup;
    return entries.slice(start, end);
  });

  const formDataGroups: FormData[] = groups.map(groupEntries => {
    const groupFormData = new FormData();
    groupEntries.forEach(([key, value]) => {
      groupFormData.append(key, value);
    });
    return groupFormData;
  });

  return formDataGroups;
}

export default SendTrainingDataButton;

/*<aside>
<h4>{acceptedFiles.length} files will uploaded</h4>
</aside>*/