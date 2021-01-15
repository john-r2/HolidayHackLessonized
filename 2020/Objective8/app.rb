# encoding: ASCII-8BIT

TMP_FOLDER = '/tmp'
FINAL_FOLDER = '/tmp'

# Don't put the uploads in the application folder
Dir.chdir TMP_FOLDER

require 'rubygems'

require 'json'
require 'sinatra'
require 'sinatra/base'
require 'singlogger'
require 'securerandom'

require 'zip'
require 'sinatra/cookies'
require 'cgi'

require 'digest/sha1'

LOGGER = ::SingLogger.instance()

MAX_SIZE = 1024**2*5 # 5mb

# Manually escaping is annoying, but Sinatra is lightweight and doesn't have
# stuff like this built in :(
def h(html)
  CGI.escapeHTML html
end

def handle_zip(filename)
  LOGGER.debug("Processing #{ filename } as a zip")
  out_files = []

  Zip::File.open(filename) do |zip_file|
    # Handle entries one by one
    zip_file.each do |entry|
      LOGGER.debug("Extracting #{entry.name}")

      if entry.size > MAX_SIZE
        raise 'File too large when extracted'
      end

      if entry.name().end_with?('zip')
        raise 'Nested zip files are not supported!'
      end

      # I wonder what this will do? --Jack
      # if entry.name !~ /^[a-zA-Z0-9._-]+$/
      #   raise 'Invalid filename! Filenames may contain letters, numbers, period, underscore, and hyphen'
      # end

      # We want to extract into TMP_FOLDER
      out_file = "#{ TMP_FOLDER }/#{ entry.name }"

      # Extract to file or directory based on name in the archive
      entry.extract(out_file) {
        # If the file exists, simply overwrite
        true
      }

      # Process it
      out_files << process_file(out_file)
    end
  end

  return out_files
end

def handle_image(filename)
  out_filename = "#{ SecureRandom.uuid }#{File.extname(filename).downcase}"
  out_path = "#{ FINAL_FOLDER }/#{ out_filename }"

  # Resize and compress in the background
  Thread.new do
    if !system("convert -resize 800x600\\> -quality 75 '#{ filename }' '#{ out_path }'")
      LOGGER.error("Something went wrong with file conversion: #{ filename }")
    else
      LOGGER.debug("File successfully converted: #{ filename }")
    end
  end

  # Return just the filename - we can figure that out later
  return out_filename
end

def process_file(filename)
  out_files = []

  if filename.downcase.end_with?('zip')
    # Append the list returned by handle_zip
    out_files += handle_zip(filename)
  elsif filename.downcase.end_with?('jpg') || filename.downcase.end_with?('jpeg') || filename.downcase.end_with?('png')
    # Append the name returned by handle_image
    out_files << handle_image(filename)
  else
    raise "Unsupported file type: #{ filename }"
  end

  return out_files
end

def process_files(files)
  return files.map { |f| process_file(f) }.flatten()
end

module TagGenerator
  class Server < Sinatra::Base
    helpers Sinatra::Cookies

    def initialize(*args)
      super(*args)
    end

    configure do
      if(defined?(PARAMS))
        set :port, PARAMS[:port]
        set :bind, PARAMS[:host]
      end

      set :raise_errors, false
      set :show_exceptions, false
    end

    error do
      return 501, erb(:error, :locals => { message: "Error in #{ __FILE__ }: #{ h(env['sinatra.error'].message) }" })
    end

    not_found do
      return 404, erb(:error, :locals => { message: "Error in #{ __FILE__ }: Route not found" })
    end

    get '/' do
      erb(:index)
    end

    post '/upload' do
      images = []
      images += process_files(params['my_file'].map { |p| p['tempfile'].path })
      images.sort!()
      images.uniq!()

      content_type :json
      images.to_json
    end

    get '/clear' do
      cookies.delete(:images)

      redirect '/'
    end

    get '/image' do
      if !params['id']
        raise 'ID is missing!'
      end

      # Validation is boring! --Jack
      # if params['id'] !~ /^[a-zA-Z0-9._-]+$/
      #   return 400, 'Invalid id! id may contain letters, numbers, period, underscore, and hyphen'
      # end

      content_type 'image/jpeg'

      filename = "#{ FINAL_FOLDER }/#{ params['id'] }"

      if File.exists?(filename)
        return File.read(filename)
      else
        return 404, "Image not found!"
      end
    end

    get '/share' do
      if !params['id']
        raise 'ID is missing!'
      end

      filename = "#{ FINAL_FOLDER }/#{ params['id'] }.png"

      if File.exists?(filename)
        erb(:share, :locals => { id: params['id'] })
      else
        return 404, "Image not found!"
      end
    end

    post '/save' do
      payload = params
      payload = JSON.parse(request.body.read)

      data_url = payload['dataURL']
      png = Base64.decode64(data_url['data:image/png;base64,'.length .. -1])

      out_hash = Digest::SHA1.hexdigest png
      out_filename = "#{ out_hash }.png"
      out_path = "#{ FINAL_FOLDER }/#{ out_filename }"
      
      LOGGER.debug("output: #{out_path}")
      File.open(out_path, 'wb') { |f| f.write(png) }
      { id: out_hash }.to_json
    end
  end
end
