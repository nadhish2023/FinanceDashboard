class python_app_server {
  package { ['python3.11', 'python3-pip', 'python3-tk', 'docker.io']:
    ensure => 'present',
  }
  service { 'docker':
    ensure  => 'running',
    enable  => true,
    require => Package['docker.io'],
  }
}
include python_app_server
