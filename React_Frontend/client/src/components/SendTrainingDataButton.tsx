//import React from 'react';
import {useDropzone} from 'react-dropzone';

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

  const files = acceptedFiles.map(f => (
    <li key={f.name}>
      {f.name}
    </li>
  ));

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
    <section className="container">
      <div {...getRootProps({className: 'dropzone'})}>
        <input {...getInputProps()} directory="" webkitdirectory="" type="file"/>
        <p>Drag 'n' drop some files here, or click to select files</p>
      </div>
      <button onClick={handleSendTrainingFiles}>Send Training Data</button>
      <aside>
        <h4>Files</h4>
        <ul>{files}</ul>
      </aside>
    </section>
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