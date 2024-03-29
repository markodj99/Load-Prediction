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
    toast.loading("Importing and preparing files.");
  
    const formData = new FormData();
    acceptedFiles.forEach(file => {
      formData.append('file', file);
    });

    try {
    const response = await fetch('/upload_and_prepare_test_files', {
        method: 'POST',
        body: formData,
    });

    if (response.ok) {
        const data = await response.json();
        toast.dismiss();
        toast.success(`Successfully imported and processed ${data.num_processed_and_writen_instance} instances.`, {duration: 8000});
    } else {
        console.error('Error while uploading and preparing the files:', response.statusText);
        toast.dismiss();
        toast.error('Error while uploading and preparing the files.', {duration: 8000});
    }
    } catch (error) {
    console.error('Error while uploading and preparing the files:', error);
    toast.dismiss();
    toast.error('Error while uploading and preparing the files.', {duration: 8000});
    }
  };

  return (
    <div className="btn-group">
      <div {...getRootProps({className: 'btn btn-outline-success dropzone d-flex justify-content-center', type:'button'})}>
        <input {...getInputProps()} directory="" webkitdirectory="" type="file"/>
        <div className="d-flex justify-content-center align-items-center text-center">
          <p className="w-100 mb-0">Select Files</p>
        </div>
      </div>
      <button type="button" className="btn btn-outline-success" onClick={handleSendTrainingFiles}>Import And Prepare Test Data</button>
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
