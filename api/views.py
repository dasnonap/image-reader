
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .forms import UploadFileForm
from .process_image import handle_file_upload, scrape_image_content

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def scrape(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if not form.is_valid():
            return Response({'msg': 'File not supported'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
                            
        file_path = handle_file_upload(request.FILES['image'])

        if not file_path:
            return Response({'msg': "Couldn't upload file"}, status=status.HTTP_500)
        
        content = scrape_image_content(file_path)
        # dd(file_path)
        
        return Response(content, status=status.HTTP_200_OK)

    return Response({'msg': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)