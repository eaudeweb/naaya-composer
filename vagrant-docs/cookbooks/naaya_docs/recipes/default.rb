require_recipe "apt"
require_recipe "nginx"


['git-core', 'python2.6-dev', 'python-virtualenv'].each do |pkg|
  package pkg do
    :upgrade
  end
end


execute "disable-default-site" do
  command "sudo nxensite default && sudo nxdissite default"
  notifies :reload, resources(:service => "nginx"), :delayed
end


template "#{node.nginx.dir}/sites-available/naaya_docs"

nginx_site "naaya_docs" do
  notifies :reload, resources(:service => "nginx"), :delayed
end
